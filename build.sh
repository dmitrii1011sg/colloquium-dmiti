#!/bin/bash

# ===========================================
#  Flet Build v0.2
#  Автор: Горшков Дмитрий 5381
# ===========================================

APP_NAME="SKA"
APP_DISPLAY_NAME="SKA"
APP_VERSION="1.0.0"
APP_COPYRIGHT="2026 Dmitrii Gorshkov"
ICON_PATH="assets/icon.png"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info()  { echo -e "${BLUE}[INFO]${NC} $1"; }
ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

clean_project() {
    info "Очистка старых артефактов сборки..."
    rm -rf build dist
    ok "Очистка завершена."
}

run_tests() {
    info "Запуск pytest..."
    if command -v pytest &> /dev/null; then
        if pytest; then
            ok "Все тесты пройдены!"
        else
            error "Тесты не пройдены. Сборка прервана."
            exit 1
        fi
    else
        warn "pytest не установлен, пропускаем тесты."
    fi
}

check_command() {
    if ! command -v "$1" &> /dev/null; then
        warn "$1 не найден. Установите $2"
        return 1
    fi
    return 0
}

check_android_sdk() {
    if [ -z "$ANDROID_HOME" ] && [ -z "$ANDROID_SDK_ROOT" ]; then
        warn "Переменные ANDROID_HOME или ANDROID_SDK_ROOT не установлены"
        return 1
    fi

    if ! check_command "adb" "Android SDK Platform Tools"; then
        return 1
    fi

    if ! check_command "java" "Java JDK 11+"; then
        return 1
    fi

    if ! adb devices | grep -q "device$"; then
        warn "Нет подключенных Android устройств или эмуляторов"
    fi

    return 0
}

OS_TYPE="unknown"
AVAILABLE_PLATFORMS=()

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS_TYPE="linux"
    AVAILABLE_PLATFORMS+=("Web (Universal)" "Linux (Native)")
    if check_command "flutter" "Flutter" && flutter build --help | grep -q "apk"; then
        AVAILABLE_PLATFORMS+=("Android (APK)")
        AVAILABLE_PLATFORMS+=("Android App Bundle (AAB)")
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS_TYPE="macos"
    AVAILABLE_PLATFORMS+=("Web (Universal)" "macOS (DMG)")
    if check_command "flutter" "Flutter" && flutter build --help | grep -q "apk"; then
        AVAILABLE_PLATFORMS+=("Android (APK)")
        AVAILABLE_PLATFORMS+=("Android App Bundle (AAB)")
    fi
    if check_command "xcodebuild" "Xcode Command Line Tools"; then
        AVAILABLE_PLATFORMS+=("iOS (IPA)")
    fi
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS_TYPE="windows"
    AVAILABLE_PLATFORMS+=("Web (Universal)" "Windows (.exe)")
    if check_command "flutter" "Flutter" && flutter build --help | grep -q "apk"; then
        AVAILABLE_PLATFORMS+=("Android (APK)")
        AVAILABLE_PLATFORMS+=("Android App Bundle (AAB)")
    fi
fi

AVAILABLE_PLATFORMS+=("Очистка проекта" "Выход")

echo "========================================="
echo -e "${GREEN}   Flet Build ${NC}"
echo "   Версия 2.0"
echo "   Приложение: $APP_NAME v$APP_VERSION"
echo "   Хост-система: $OS_TYPE"
echo "========================================="

if [ ${#AVAILABLE_PLATFORMS[@]} -gt 2 ]; then
    PS3="Выберите целевые платформы (введите номер): "
    select opt in "${AVAILABLE_PLATFORMS[@]}"
    do
        case $opt in
            "Web (Universal)")
                clean_project
                run_tests
                info "Сборка Web-версии..."
                flet build web --product "$APP_NAME" --base-url "/" --route-url-strategy "path"
                ok "Web-версия собрана в папке build/web"
                ;;
            "Linux (Native)")
                if [ "$OS_TYPE" != "linux" ]; then
                    error "Linux-сборка возможна только на Linux."
                    continue
                fi
                clean_project
                info "Сборка Linux-приложения..."
                flet build linux --product "$APP_NAME" --copyright "$APP_COPYRIGHT"
                ok "Linux-приложение собрано в build/linux"
                ;;
            "Windows (.exe)")
                if [ "$OS_TYPE" != "windows" ]; then
                    error "Windows-сборка возможна только на Windows."
                    continue
                fi
                clean_project
                info "Сборка Windows-приложения..."
                flet build windows --product "$APP_NAME" --copyright "$APP_COPYRIGHT" --company-name "YourCompany"
                ok "Windows-приложение собрано в build/windows"
                ;;
            "macOS (DMG)")
                if [ "$OS_TYPE" != "macos" ]; then
                    error "macOS-сборка возможна только на macOS."
                    continue
                fi
                clean_project
                info "Сборка macOS-приложения..."
                flet build macos --product "$APP_NAME" --copyright "$APP_COPYRIGHT" --build-version "$APP_VERSION"
                ok "macOS-приложение собрано в build/macos"
                ;;
            "iOS (IPA)")
                if [ "$OS_TYPE" != "macos" ]; then
                    error "iOS-сборка возможна только на macOS с Xcode."
                    continue
                fi
                clean_project
                info "Сборка iOS-приложения (потребуется Apple Developer аккаунт)..."
                flet build ios --product "$APP_NAME" --build-version "$APP_VERSION"
                ok "iOS-приложение собрано в build/ios"
                ;;
            "Android (APK)")
                if ! check_android_sdk; then
                    error "Android SDK не настроен. Сборка невозможна."
                    echo "Установите Android Studio и настройте переменные окружения:"
                    echo "export ANDROID_HOME=\$HOME/Android/Sdk"
                    echo "export PATH=\$PATH:\$ANDROID_HOME/emulator:\$ANDROID_HOME/platform-tools"
                    continue
                fi
                clean_project
                info "Сборка Android APK (кеширование может занять время)..."
                flet build apk --product "$APP_NAME" --version-name "$APP_VERSION" --copyright "$APP_COPYRIGHT"
                ok "APK готов: build/app/outputs/flutter-apk/app-release.apk"
                ;;
            "Android App Bundle (AAB)")
                if ! check_android_sdk; then
                    error "Android SDK не настроен. Сборка невозможна."
                    continue
                fi
                clean_project
                info "Сборка Android App Bundle (для Google Play)..."
                flet build aab --product "$APP_NAME" --version-name "$APP_VERSION" --copyright "$APP_COPYRIGHT"
                ok "AAB готов: build/app/outputs/bundle/release/app-release.aab"
                ;;
            "Очистка проекта")
                clean_project
                ;;
            "Выход")
                echo "Выход из скрипта..."
                exit 0
                ;;
            *)
                error "Неверный выбор. Попробуйте снова."
                ;;
        esac
        echo
        read -p "Нажмите Enter, чтобы продолжить или Ctrl+C для выхода..."
        echo
        PS3="Выберите следующее действие: "
    done
else
    warn "Обнаружена только одна доступная платформа: ${AVAILABLE_PLATFORMS[0]}"
    read -p "Запустить сборку? (y/n): " yn
    if [[ $yn == "y" ]]; then
        echo "Запуск сборки..."
        exit 0
    fi
fi

echo "========================================="
echo -e "${GREEN}   Все операции завершены!${NC}"
echo "========================================="
