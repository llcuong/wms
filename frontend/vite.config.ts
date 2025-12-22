import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from "@tailwindcss/vite";
import path from "path";

export default defineConfig({
    plugins: [react(), tailwindcss()],
    resolve: {
        alias: {
            "@routes/configs": path.resolve(__dirname, "src/routes/configs"),
            "@routes/navigation": path.resolve(__dirname, "src/routes/navigation"),
            "@routes/utils": path.resolve(__dirname, "src/routes/utils"),
            "@routes/types": path.resolve(__dirname, "src/routes/types"),

            "@global/types": path.resolve(__dirname, "src/types"),

            "@layouts": path.resolve(__dirname, "src/shared/layouts"),
            "@icons": path.resolve(__dirname, "src/shared/icons"),
            "@hooks": path.resolve(__dirname, "src/shared/hooks"),
            "@components": path.resolve(__dirname, "src/shared/components"),
            "@modules": path.resolve(__dirname, "src/shared/modules"),
            "@store": path.resolve(__dirname, "src/shared/stores"),

            "@former": path.resolve(__dirname, "src/apps/former"),
            "@semi-finished": path.resolve(__dirname, "src/apps/semi-finished"),
            "@finished": path.resolve(__dirname, "src/apps/finished"),
        },
    },
    server: {
        host: true,
        port: 10000,
    },
    build: {
        target: "esnext",
    },
})
