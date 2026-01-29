# Mobile Wrapper for AI Music Generator

This directory contains the Capacitor-based mobile app wrapper for deploying the AI Music Generator to Android and iOS via Google Play Store and Apple App Store.

## Setup

### Prerequisites
- Node.js 16+ and npm
- Android Studio (for Android)
- Xcode (for iOS)
- Capacitor CLI: `npm install -g @capacitor/cli`

### Install Dependencies

```bash
cd mobile
npm install
```

### Build Web Assets

```bash
npm run build:web
```

### Add Platforms

```bash
# Android
npx cap add android

# iOS (macOS only)
npx cap add ios
```

### Sync Changes

```bash
npx cap sync
```

### Build for Android

```bash
cd android
./gradlew assembleRelease
```

Signed APK will be in: `android/app/build/outputs/apk/release/app-release.apk`

### Upload to Google Play Console

1. Go to [Google Play Console](https://play.google.com/console)
2. Create a new app: "AI Music Generator"
3. Upload APK/AAB to Internal Testing → Production
4. Fill in app details:
   - **Title**: AI Music Generator
   - **Short Description**: Create music and vocals with AI
   - **Full Description**: [See STORE_LISTING.md]
   - **Screenshots**: (4–8 screenshots from the app)
   - **Privacy Policy**: (link to privacy.md)
   - **Category**: Music & Audio
   - **Rating**: Self-classified content rating

## Configuration

Edit `mobile/capacitor.config.ts` to customize:
- App name and ID
- Version number
- Splash screen
- Permissions

## Debugging

```bash
# iOS Simulator
npx cap open ios

# Android Emulator
npx cap open android

# Live reload (dev mode)
npm run serve
```

## Troubleshooting

- **Camera not loading**: Check `AndroidManifest.xml` permissions
- **Audio not working**: Ensure `RECORD_AUDIO` permission is granted
- **Build fails**: Run `npx cap sync` and rebuild

## Release Checklist

- [ ] Update version in `capacitor.config.ts`
- [ ] Test on physical device
- [ ] Generate signed APK
- [ ] Update app screenshots
- [ ] Write release notes
- [ ] Submit to Google Play for review
