# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A bilingual (English/Spanish) static web application that displays a daily common misconception. The app shows one misconception per day using localStorage to track which misconceptions have been shown and ensure users see each one before repeating.

## Architecture

### Core Components

- **[index.html](index.html)**: Single-page application structure with three-column layout (ads on sides, content in center)
- **[app.js](app.js)**: Contains all application logic and data
- **[style.css](style.css)**: Styling with animated starfield background and glassmorphic UI

### Data Structure

Misconceptions are stored as two hardcoded arrays in [app.js](app.js):
- `misconceptions_en`: English misconceptions (29 items)
- `misconceptions_es`: Spanish misconceptions (19 items)

### State Management

Uses browser localStorage with language-specific keys:
- `daily_data_{lang}`: Stores `{ index, date }` for the current day's misconception
- `shown_{lang}`: Array of indices for misconceptions already displayed

### Key Logic Flow

1. On load, app detects browser language (`navigator.language`) and sets initial language
2. `showDailyMisconception()` checks if date changed:
   - If new day: selects random misconception from pool of unshown items
   - If same day: displays same misconception
3. When all misconceptions shown, the `shown` array resets
4. Language toggle fades out current text, switches language, updates UI, and fades in new text

## Development

This is a vanilla JavaScript project with no build process or dependencies. Simply open [index.html](index.html) in a browser to run.

### Testing Changes

Open [index.html](index.html) in a browser. To reset localStorage during testing:
```javascript
localStorage.clear()
```

### Adding New Misconceptions

Add new entries to `misconceptions_en` or `misconceptions_es` arrays in [app.js](app.js). Arrays can have different lengths per language.
