const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Enable CORS and permissive headers for iframe and preview proxying
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', '*');
  res.removeHeader('X-Frame-Options');
  next();
});

// Serve static assets
app.use(express.static(path.join(__dirname, 'public')));
app.use('/output', express.static(path.join(__dirname, '..', 'output')));
app.use('/audio', express.static(path.join(__dirname, '..', 'audio')));
app.use('/assets', express.static(path.join(__dirname, '..', 'assets')));
app.use('/snapshots', express.static(path.join(__dirname, '..', 'rendered_snapshots')));

// API endpoint for metadata
app.get('/api/metadata', (req, res) => {
  res.json({
    title: "Projapati Matrimonial Official Commercial Ad",
    website: "www.projapati.in.net",
    tagline: "Where Two Souls Meet",
    duration: 51.5,
    resolution: "1920x1080 (1080p Full HD)",
    fps: 30,
    videoUrl: "/output/projapati_matrimonial_ad.mp4",
    audioUrl: "/audio/master_audio.wav",
    scenes: [
      {
        id: 1,
        timecode: "00:00 - 00:08",
        start: 0,
        end: 8.5,
        title: "The Sacred Dream",
        subhead: "Every Great Love Story Begins With A Dream",
        description: "Cinematic opening with the ethereal glowing golden Projapati butterfly fluttering through traditional Indian wedding lamps and marigold garlands.",
        voiceover: "Every great love story begins with a single dream: finding the one who truly completes you.",
        thumbnail: "/snapshots/frame_scene1.jpg"
      },
      {
        id: 2,
        timecode: "00:08 - 00:18",
        start: 8.5,
        end: 18.2,
        title: "100% Verified Profiles",
        subhead: "Trust, Authenticity & Family Values",
        description: "Smart, cultured bride and groom profile showcase highlighting verified identity, family values, and safety.",
        voiceover: "Welcome to Projapati Matrimony. Explore thousands of genuine, verified profiles crafted with trust and family values.",
        thumbnail: "/snapshots/frame_scene2.jpg"
      },
      {
        id: 3,
        timecode: "00:18 - 00:27",
        start: 18.2,
        end: 27.2,
        title: "Chemistry & Compatibility",
        subhead: "Find Your Perfect Soulmate",
        description: "Joyful modern couple connecting warmly over tea in a festive garden cafe with radiant smiles and true compatibility.",
        voiceover: "Discover someone who shares your culture, aspirations, and life goals, with complete privacy and intelligent matchmaking.",
        thumbnail: "/snapshots/frame_scene3.jpg"
      },
      {
        id: 4,
        timecode: "00:27 - 00:36",
        start: 27.2,
        end: 36.2,
        title: "Sacred Wedding Ceremony",
        subhead: "A Sacred Bond Of Togetherness",
        description: "Opulent royal Indian wedding mandap ceremony with the couple exchanging rose and jasmine garlands showered in red rose petals.",
        voiceover: "Turn beautiful moments into a sacred bond of togetherness, uniting two hearts and two families forever.",
        thumbnail: "/snapshots/frame_scene4.jpg"
      },
      {
        id: 5,
        timecode: "00:36 - 00:51",
        start: 36.2,
        end: 51.5,
        title: "Grand Outro & Call to Action",
        subhead: "Begin Your Forever Story Today",
        description: "Spectacular fireworks celebration leading into the iconic 3D golden Projapati butterfly emblem and direct website CTA.",
        voiceover: "Your happily ever after starts today. Register for free now at www dot projapati dot in dot net. Projapati Matrimony: where two souls meet.",
        thumbnail: "/snapshots/frame_scene5a.jpg"
      }
    ]
  });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Projapati Ad Video Showcase server running at http://0.0.0.0:${PORT}`);
});
