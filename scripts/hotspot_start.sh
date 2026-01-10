#!/bin/bash
set -e

# Configuration Paths
REPO_ROOT=$(dirname "$(dirname "$(readlink -f "$0")")")
CONFIG_DIR="$REPO_ROOT/scripts/config"

echo "🔥 Starting Hotspot..."

# 1. Stop existing services to avoid conflicts
echo "   Stopping potentially conflicting services..."
systemctl stop dnsmasq || true
systemctl stop hostapd || true
killall hostapd 2>/dev/null || true
killall dnsmasq 2>/dev/null || true

killall hostapd 2>/dev/null || true
killall dnsmasq 2>/dev/null || true


# 2. Configure Interface
echo "   Configuring wlan0 IP..."
ifconfig wlan0 down || true
ifconfig wlan0 up
ifconfig wlan0 192.168.4.1 netmask 255.255.255.0

# 3. Start Hostapd
echo "   Starting hostapd..."
hostapd -B "$CONFIG_DIR/hostapd.conf"

# 4. Start Dnsmasq
echo "   Starting dnsmasq..."
dnsmasq -C "$CONFIG_DIR/dnsmasq.conf"

# 5. Enable Packet Forwarding (Just in case)
sysctl -w net.ipv4.ip_forward=1 > /dev/null

# 6. Captive Portal Rules (The Trap)
echo "   Applying IPTables rules..."
# Redirect HTTP (80) to FastAPI (8000)
iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 80 -j DNAT --to-destination 192.168.4.1:8000
# Note: HTTPS (443) redirection usually causes SSL errors, but ensures traffic doesn't escape.
# For a friendly kiosk, we often leave it or redirect to a self-signed cert port. 
# Here we redirect to 8000 (HTTP) which will fail SSL handshake but trap the connection.
iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 443 -j DNAT --to-destination 192.168.4.1:8000

echo "✅ Hotspot 'CopyFlow-Print' is active."

