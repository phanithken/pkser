# Server Automation CLI

## Description

Server Automation CLI is a powerful command-line interface tool designed to streamline and automate repetitive tasks on servers. This tool currently focuses on Nginx and Laravel configurations, providing easy-to-use commands for setting up web servers and managing basic authentication.

The primary goals of this project are to:

1. Simplify the process of setting up Nginx for Laravel applications
2. Provide an efficient way to manage basic authentication for Nginx servers
3. Reduce human error in server configuration tasks
4. Save time for system administrators and developers

## Features

- **Nginx and Laravel Setup**: Quickly configure Nginx for a Laravel application on a new server instance.
- **Basic Authentication Management**: Add or remove basic authentication for specific domains in Nginx.
- **Error Handling**: Robust error checking to prevent server misconfigurations.
- **Configuration Backups**: Automatic backups of Nginx configurations before making changes.
- **Telegram Notifications**: Optional integration with Telegram for real-time notifications on task completion or errors.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/server-automation-cli.git
   ```
2. Navigate to the project directory:
   ```
   cd server-automation-cli
   ```
3. Make the scripts executable:
   ```
   chmod +x *.sh
   ```

## Usage

### Nginx and Laravel Setup

To set up Nginx for a Laravel application:

```
./nginx_laravel_setup.sh <domain>
```

Replace `<domain>` with your actual domain name.

### Basic Authentication Management

To add basic authentication:

```
./nginx_auth_manager.sh add <domain> <username> <password>
```

To remove basic authentication:

```
./nginx_auth_manager.sh remove <domain>
```

### Telegram Notifications

To enable Telegram notifications, set the following environment variables:

```
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
```

You can add these to your shell configuration file (e.g., `~/.bashrc` or `~/.zshrc`) for persistence.

## Configuration

The scripts use default paths for Nginx configurations. If your server uses different paths, you may need to modify the scripts accordingly.

## Contributing

Contributions to the Server Automation CLI are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Thanks to all contributors who have helped shape this project.
- Special thanks to the Nginx and Laravel communities for their excellent documentation.

## Disclaimer

These scripts make changes to your server configuration. Always test in a non-production environment first and ensure you have backups before running them on a live server.

