#!/bin/bash
# Usage ./nginx_auth_manager.sh add example.com username password
# ./nginx_auth_manager.sh remove example.com

# Function to display usage information
usage() {
    echo "Usage: $0 [add|remove] <domain> [username] [password]"
    echo "  add    - Add basic authentication to the specified domain"
    echo "  remove - Remove basic authentication from the specified domain"
    echo "  <domain> - The domain to modify"
    echo "  [username] - Required when adding authentication"
    echo "  [password] - Required when adding authentication"
    exit 1
}

# Function to test Nginx configuration
test_nginx_config() {
    echo "Testing Nginx configuration..."
    if ! sudo nginx -t; then
        echo "Error: Nginx configuration test failed. Rolling back changes..."
        if [ -f "/etc/nginx/sites-available/${DOMAIN}.bak" ]; then
            sudo mv "/etc/nginx/sites-available/${DOMAIN}.bak" "/etc/nginx/sites-available/${DOMAIN}"
            echo "Configuration rolled back. Please check your Nginx configuration manually."
        else
            echo "Backup file not found. Manual intervention required."
        fi
        exit 1
    fi
    echo "Nginx configuration test passed."
}

# Function to reload Nginx
reload_nginx() {
    echo "Reloading Nginx..."
    if ! sudo systemctl reload nginx; then
        echo "Error: Failed to reload Nginx. Please check Nginx status and logs."
        exit 1
    fi
    echo "Nginx reloaded successfully."
}

# Check for correct number of arguments
if [ "$1" = "add" ] && [ $# -ne 4 ]; then
    usage
elif [ "$1" = "remove" ] && [ $# -ne 2 ]; then
    usage
fi

ACTION=$1
DOMAIN=$2
USERNAME=$3
PASSWORD=$4

NGINX_CONF="/etc/nginx/sites-available/${DOMAIN}"
AUTH_FILE="/etc/nginx/.htpasswd-${DOMAIN}"

# Check if the Nginx configuration file exists
if [ ! -f "$NGINX_CONF" ]; then
    echo "Error: Nginx configuration file for ${DOMAIN} not found."
    exit 1
fi

# Create a backup of the original configuration
sudo cp "$NGINX_CONF" "${NGINX_CONF}.bak"

case $ACTION in
    add)
        # Check if .htpasswd file already exists
        if [ -f "$AUTH_FILE" ]; then
            echo "Warning: .htpasswd file already exists for ${DOMAIN}."
            read -p "Do you want to overwrite it? (y/n): " overwrite
            if [[ $overwrite =~ ^[Yy]$ ]]; then
                echo "Overwriting existing .htpasswd file..."
                sudo htpasswd -cb "$AUTH_FILE" "$USERNAME" "$PASSWORD"
            else
                echo "Operation aborted. Existing .htpasswd file not modified."
                exit 0
            fi
        else
            sudo htpasswd -cb "$AUTH_FILE" "$USERNAME" "$PASSWORD"
        fi

        # Add auth_basic directives to Nginx config if not already present
        if ! grep -q "auth_basic" "$NGINX_CONF"; then
            sudo sed -i '/server_name/a\    auth_basic "Restricted Area";\n    auth_basic_user_file '"$AUTH_FILE"';' "$NGINX_CONF"
        else
            echo "Basic authentication directives already present in Nginx config."
        fi
        ;;

    remove)
        # Remove auth_basic directives from Nginx config
        sudo sed -i '/auth_basic/d' "$NGINX_CONF"
        
        # Remove .htpasswd file if it exists
        if [ -f "$AUTH_FILE" ]; then
            sudo rm "$AUTH_FILE"
        fi
        ;;

    *)
        usage
        ;;
esac

# Test and reload Nginx
test_nginx_config
reload_nginx

echo "Basic authentication has been ${ACTION}ed for ${DOMAIN}."