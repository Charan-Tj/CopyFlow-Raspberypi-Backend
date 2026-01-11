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
killall wpa_supplicant 2>/dev/null || true

echo "   Stopping Network Managers..."
systemctl stop NetworkManager 2>/dev/null || true
systemctl stop wpa_supplicant 2>/dev/null || true
systemctl stop dhcpcd 2>/dev/null || true


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
# Note: We do NOT redirect 443 (HTTPS) to 8000 anymore.
# Redirecting HTTPS to HTTP causes "Invalid HTTP request" errors in logs because
# the browser sends encrypted SSL "Hello" packets which our HTTP server cannot understand.
# By dropping/ignoring 443, the phone will quickly fail HTTPS and fallback to HTTP, which we catch below.
# iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 443 -j DNAT --to-destination 192.168.4.1:8000

echo "✅ Hotspot 'CopyFlow-Print' is active."

