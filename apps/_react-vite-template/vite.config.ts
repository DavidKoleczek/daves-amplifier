// @ts-expect-error path module is available at build time
import path from "path";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      // @ts-expect-error __dirname is available at runtime in Vite
      // eslint-disable-next-line
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
