/** @type {import('tailwindcss').Config} */

const {nextui} = require("@nextui-org/react");

module.exports = {
    // corePlugins: {
    //     preflight: false,
    //            },
    content: [
        "./src/**/*.{js,jsx,ts,tsx}",
        "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}",
        './node_modules/@nextui-org/theme/dist/components/(button|snippet|code|input).js'
    ],
    theme: {
      extend: {},
    },
    plugins: [
        nextui({
          addCommonColors: true,
        }),
      ],
    darkMode: "class",
    // important: true,
  };
