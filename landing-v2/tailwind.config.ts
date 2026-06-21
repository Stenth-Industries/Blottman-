import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Black-and-gold palette modelled on gardewilson.com.au
        ink: {
          DEFAULT: "#0c0c0c", // near-black — primary dark surface
          soft: "#171717",
          line: "#262626",
          muted: "#6b6b6b",
        },
        gold: {
          DEFAULT: "#e7ac40", // primary brand gold
          bright: "#f5c03d", // highlight gold
          deep: "#d99944", // deeper amber
          soft: "#fadd99", // pale gold tint
        },
        paper: "#fffbf7", // warm off-white background
      },
      fontFamily: {
        // Anton ≈ "Thunder" (heavy condensed display); Poppins for body/UI
        display: ["var(--font-anton)", "Impact", "sans-serif"],
        sans: ["var(--font-poppins)", "system-ui", "sans-serif"],
      },
      maxWidth: {
        content: "1400px",
      },
      backgroundImage: {
        // Metallic-gold ramp lifted from gardewilson.com.au — the pale champagne
        // highlight band (#fadd99) through the middle is what makes it read as
        // brushed metal rather than a flat fill. Used on key words + buttons.
        "gold-sheen":
          "linear-gradient(103deg, #f5c03d 0%, #fadd99 30%, #fadf9e 58%, #f5c03d 88%)",
        // Rich metallic gold for the outline button's text on hover — uniform
        // gold with a subtle bright sheen (no pale champagne band), matching the
        // all-gold hover reference (image copy 5.png).
        "gold-sheen-hover":
          "linear-gradient(103deg, #e7ac40 0%, #f3c75e 45%, #d99944 100%)",
      },
      keyframes: {
        "fade-up": {
          "0%": { opacity: "0", transform: "translateY(18px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        marquee: {
          "0%": { transform: "translateX(0)" },
          "100%": { transform: "translateX(-50%)" },
        },
      },
      animation: {
        "fade-up": "fade-up 0.6s ease-out both",
        marquee: "marquee 28s linear infinite",
      },
    },
  },
  plugins: [],
};

export default config;
