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
        content: "1180px",
      },
      backgroundImage: {
        // Restrained metallic-gold sweep, used only on key words/buttons
        "gold-sheen": "linear-gradient(100deg, #f5c03d 0%, #e7ac40 45%, #d99944 100%)",
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
