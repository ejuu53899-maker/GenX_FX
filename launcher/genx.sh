#!/usr/bin/env bash
set -euo pipefail

COMMAND="${1:-help}"

case "$COMMAND" in

    start)
        ./launcher/start.sh
        ;;

    stop)
        ./launcher/stop.sh
        ;;

    restart)
        ./launcher/stop.sh 2>/dev/null || true
        ./launcher/start.sh
        ;;

    health)
        ./launcher/health_check.sh
        ;;

    status)
        ./launcher/health_check.sh
        ;;

    extensions)
        echo "Installed GENX extensions:"
        find skills -mindepth 1 -maxdepth 2 -name manifest.yaml \
            -print 2>/dev/null || true
        ;;

    install-extension)
        if [ -z "${2:-}" ]; then
            echo "Usage: ./launcher/genx.sh install-extension <path>"
            exit 1
        fi

        ./scripts/install_extension.sh "$2"
        ;;

    update)
        ./launcher/update.sh
        ;;

    emergency-stop)
        ./launcher/emergency_stop.sh
        ;;

    help|*)
        echo "GENX Starter Kit v3.6.9"
        echo
        echo "Commands:"
        echo "  start"
        echo "  stop"
        echo "  restart"
        echo "  status"
        echo "  health"
        echo "  extensions"
        echo "  install-extension <path>"
        echo "  update"
        echo "  emergency-stop"
        ;;

esac
