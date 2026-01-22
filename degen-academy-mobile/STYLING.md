# Degen Academy Styling Guide

## Fonts

| Font | Class | Usage |
|------|-------|-------|
| **Fredoka One** | `font-chalk` | Titles, headers, playful labels |
| **Patrick Hand** | `font-handwritten` | Ralph quotes, witty messages, taglines |
| **JetBrains Mono** | `font-mono` | Numbers, stats, money values |
| **Inter** | default | Body text, UI labels |

## Colors

### Background
- Dark base: `#0a0a14` / `var(--color-bg-dark)`
- Panels: `#2d2d3a`
- Cards: `#3d3d4a`
- Input backgrounds: `#252532`

### Accent Colors
- Green (success/farming): `#4ade80`
- Yellow (warning/gold): `#fbbf24`
- Blue (info/charts): `#60a5fa`
- Purple (Ralph/special): `#a78bfa`
- Red (danger/rekt): `#f87171`
- Cyan (progress): `#22d3ee`

## Crayon Button Style (MenuScreen)
```css
.play-btn {
  color: #2D3436;
  background: #FFD93D;
  border: 3px solid #2D3436;
  border-radius: 10px;
  box-shadow: 3px 3px 0px #2D3436;
}
.play-btn:hover {
  transform: translate(2px, 2px);
  box-shadow: 2px 2px 0px #2D3436;
}
```

## Thought Bubble Style
```css
.section-bubble {
  background: white;
  border: 3px solid #2D3436;
  border-radius: 20px;
  box-shadow: 3px 3px 0px #2D3436;
}
```

## Info Box Hover Effects
```css
.info-box:nth-child(1):hover { transform: rotate(1deg) translateY(-4px); }
.info-box:nth-child(2):hover { transform: rotate(-1deg) translateY(-4px); }
.info-box:nth-child(3):hover { transform: rotate(1deg) translateY(-4px); }
```

## Neumorphic Buttons (GameScreen)
```css
.neu-btn {
  background: #3a3a4a;
  box-shadow: 3px 3px 6px #1e1e28, -2px -2px 5px #4a4a5a;
}
.neu-btn:active {
  box-shadow: inset 3px 3px 6px #1e1e28, inset -2px -2px 5px #4a4a5a;
}
```

## Where to Use Each Font

### Chalk Font (font-chalk)
- Main titles: "Ralph's Degen Academy"
- Section headers: "Liquidity Pools"
- Feature names: "Yield Farming", "Risk Management", "DeFi Mechanics"
- Button text: "Enter the Lab"

### Handwritten Font (font-handwritten)
- Ralph's quotes
- Taglines: "Learn DeFi by getting rekt (safely)"
- Footer messages
- Witty one-liners

### Mono Font (font-mono)
- Wallet balance
- APY percentages
- Timer countdowns
- Portfolio values
- Stats numbers

## SVG Icons
Use white stroke icons (`stroke="currentColor"`) with `stroke-width="1.8"` for clean, handmade look.
