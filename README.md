# Common Misconceptions / Falsos Mitos

A bilingual daily misconception web app that displays fascinating facts debunking common myths.

## Features

- **456 English** and **334 Spanish** misconceptions sourced from Wikipedia
- **Daily rotation** - New misconception every day based on local timezone
- **Bilingual** - Switch between English and Spanish
- **Dark/Light mode** - User preference saved locally
- **Streak tracking** - Track consecutive daily visits
- **Weekly bonus** - Extra misconception once per week
- **Social sharing** - Share on Twitter, Facebook, WhatsApp, Reddit
- **Progress tracking** - See how many misconceptions you've explored
- **Responsive design** - Works on all devices
- **No backend required** - Pure client-side JavaScript

## Running Locally

**IMPORTANT**: This app requires a web server to run properly. Opening `index.html` directly (`file://`) won't work due to CORS restrictions when loading JSON files.

### Option 1: Python (Recommended)

```bash
# Navigate to project directory
cd "/Users/eliashernandezramon/Documents/MBP14-Documents/Webdev Projects/Common_misconceptions"

# Python 3
python3 -m http.server 8000

# Then open http://localhost:8000 in your browser
```

### Option 2: Node.js

```bash
# Install http-server globally
npm install -g http-server

# Run server
http-server -p 8000

# Then open http://localhost:8000 in your browser
```

### Option 3: VS Code Live Server

1. Install "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

## File Structure

```
Common_misconceptions/
├── index.html          # Main HTML file
├── style.css           # Styles with CSS variables for theming
├── app.js              # Application logic
├── data/
│   ├── misconceptions_en.json  # 456 English misconceptions
│   └── misconceptions_es.json  # 334 Spanish misconceptions
├── CLAUDE.md           # AI assistant context
└── README.md           # This file
```

## Data Sources

All misconceptions are sourced from Wikipedia:

**English:**
- [List of common misconceptions about arts and culture](https://en.wikipedia.org/wiki/List_of_common_misconceptions_about_arts_and_culture)
- [List of common misconceptions about history](https://en.wikipedia.org/wiki/List_of_common_misconceptions_about_history)
- [List of common misconceptions about science, technology, and mathematics](https://en.wikipedia.org/wiki/List_of_common_misconceptions_about_science,_technology,_and_mathematics)

**Spanish:**
- [Anexo:Falsos mitos](https://es.wikipedia.org/wiki/Anexo:Falsos_mitos)

## Technologies Used

- Vanilla JavaScript (ES6+)
- CSS3 with CSS Variables
- localStorage for persistence
- Fetch API for loading JSON data
- Web Share API for mobile sharing

## Deployment to GitHub Pages

1. Commit all files to your repository
2. Go to repository Settings > Pages
3. Select branch `main` and folder `/ (root)`
4. Save and wait for deployment
5. Your site will be available at `https://yourusername.github.io/repository-name/`

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## License

Data sourced from Wikipedia under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)

## Support

Support this project: [Buy Me a Coffee](https://buymeacoffee.com/eliaschao)
