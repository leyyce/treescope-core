# Nimmt zwei Parameter: Domain-Name und E-Mail-Adresse
param (
    [string]$DOMAIN,
    [string]$EMAIL
)
if(-not(Test-path .env -PathType leaf)) {
    Write-Host "Creating .env file..."

    # Generiere zufällige Passwörter und Schlüssel mit openssl und entferne Linebreaks
    $POSTGRES_PASSWORD = & openssl rand -base64 60 | Out-String
    $POSTGRES_PASSWORD = $POSTGRES_PASSWORD -replace "\r|\n", ""

    $SECRET_KEY = & openssl rand -base64 60 | Out-String
    $SECRET_KEY = $SECRET_KEY -replace "\r|\n", ""

    # Schreibe die Variablen in die .env Datei
    @"
    POSTGRES_DB=treescope
    POSTGRES_USER=treescope-user
    POSTGRES_PASSWORD=$POSTGRES_PASSWORD
    SECRET_KEY=$SECRET_KEY
    DOMAIN=$DOMAIN
    EMAIL=$EMAIL
"@ | Set-Content -Path .env
    Write-Host ".env file created successfully!"
 }


# Create a temporary OpenSSL config file
$configPath = "openssl.cfg"
$configContent = @"
[dn]
CN=localhost

[req]
distinguished_name = dn

[EXT]
subjectAltName=DNS:localhost
keyUsage=digitalSignature
extendedKeyUsage=serverAuth
"@
$configContent | Set-Content -Path $configPath

curl -L --create-dirs -o etc/letsencrypt/options-ssl-nginx.conf https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf
if(-not(Test-path etc\letsencrypt\live\${DOMAIN}\)) {
    New-Item -ItemType Directory -Path etc\letsencrypt\live\${DOMAIN}\
}

# Run OpenSSL command
openssl req -x509 -out etc\letsencrypt\live\${DOMAIN}\fullchain.pem -keyout .\etc\letsencrypt\live\${DOMAIN}\privkey.pem -newkey rsa:2048 -nodes -sha256 -subj '/CN=localhost' -extensions EXT -config $configPath

openssl dhparam -out etc\letsencrypt\ssl-dhparams.pem 2048

# Optionally, clean up the config file after use
Remove-Item -Path $configPath