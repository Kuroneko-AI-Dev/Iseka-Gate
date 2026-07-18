import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";
import path from "path";

export default defineConfig({

    plugins:[

        react(),

        VitePWA({

            registerType:"autoUpdate",

            injectRegister:"auto",

            includeAssets:[

                "favicon.ico",
                "apple-touch-icon.png"

            ],

            manifest:{

                name:"AOI CHISEI",

                short_name:"AOI",

                description:"AI Companion",

                theme_color:"#111827",

                background_color:"#111827",

                display:"standalone",

                orientation:"portrait",

                start_url:"/",

                scope:"/",

                icons:[

                    {
                        src:"/pwa-192.png",
                        sizes:"192x192",
                        type:"image/png"
                    },

                    {
                        src:"/pwa-512.png",
                        sizes:"512x512",
                        type:"image/png"
                    },

                    {
                        src:"/pwa-512.png",
                        sizes:"512x512",
                        type:"image/png",
                        purpose:"maskable"
                    }

                ]

            }

        })

    ],

    resolve:{

        alias:{

            "@framework":path.resolve(__dirname,"src/framework"),

            "@live2d":path.resolve(__dirname,"src/live2d")

        }

    }

});