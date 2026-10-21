# MinorShield — Frontend (Android) — Notice

Projet **Android natif (Kotlin)** contenant **deux applications** dans un seul projet Gradle :

- **`app/`** → application **Parent** (`com.minorshield`)
- **`app-enfant/`** → application **Enfant** (`com.minorshield.enfant`)

## Ouvrir le projet
Ouvrir le dossier **`app-parent/`** avec **Android Studio** (Giraffe ou plus récent).
Android Studio génère lui-même `local.properties` (chemin du SDK) au premier lancement.

## Adresse du backend (à mettre à jour après migration)
L'URL du serveur est **codée en dur** dans une seule constante par application :

- Parent : `app/src/main/java/com/minorshield/network/ParentApiClient.kt` → `BASE_URL`
- Enfant : `app-enfant/src/main/java/com/minorshield/enfant/network/ChildApiClient.kt` → `BASE_URL`

Après avoir changé de serveur, remplacer ces deux `BASE_URL` par la nouvelle URL
(doit finir par `/`), puis regénérer les APK. La clé `API_KEY` (dans `ChildApiClient.kt`)
doit correspondre à celle du backend (`CHANGE_ME`).

## Générer les APK
```bash
# Debug (installable directement, non signé pour la prod)
./gradlew :app:assembleDebug :app-enfant:assembleDebug

# Release (signé) — nécessite un keystore + un fichier keystore.properties
./gradlew :app:assembleRelease :app-enfant:assembleRelease
```
Sorties : `<module>/build/outputs/apk/{debug|release}/`.

## Signature release (non incluse)
La configuration de signature lit un fichier **`keystore.properties`** (+ le keystore),
**volontairement non fournis** dans ce zip (ce sont des identifiants de signature
sensibles). Sans eux, les builds `release` restent non signés — utiliser `assembleDebug`
pour tester, ou fournir votre propre keystore.

## Firebase
Le fichier `app/google-services.json` (config Firebase du Parent) est inclus : il est
nécessaire à la compilation. Les notifications push côté serveur nécessitent en plus
une clé de compte de service Firebase (côté backend).
