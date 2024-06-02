// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { remarkKroki } from 'remark-kroki';
import rehypeRaw from 'rehype-raw';


/** @type {import('@docusaurus/types').Config} */
const config = {
  title: '玩具帝国',
  tagline: 'Toy Empires',
  favicon: '/img/icon.ico',
  staticDirectories: ['public', 'static'],
  // Set the production url of your site here
  url: 'https://your-docusaurus-site.example.com',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'facebook', // Usually your GitHub org/user name.
  projectName: 'docusaurus', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  
  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'zh-Hans',
    locales: ['zh-Hans'],
  },

  plugins: [
    [ require.resolve('docusaurus-lunr-search'), {
        languages: ['zh'], // language codes,
        excludeRoutes:['blog']
      }],
    require.resolve("docusaurus-plugin-image-zoom"),
    async function myPlugin(context, options) {
        return {
          name: "docusaurus-tailwindcss",
          configurePostCss(postcssOptions) {
            // Appends TailwindCSS and AutoPrefixer.
            postcssOptions.plugins.push(require("tailwindcss"));
            postcssOptions.plugins.push(require("autoprefixer"));
            return postcssOptions;
          },
        };
      },
],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          remarkPlugins: [
            remarkMath,
            [
                remarkKroki,
                {
                  server: 'https://kroki.io',
                  alias: ['mermaid','graphviz'],
                  target: 'mdx3',
                  output: 'img-html-base64'
                }
              ],
          ],
          rehypePlugins: [
            rehypeKatex,
            [
                rehypeRaw,
                {
                  passThrough: [
                    'mdxFlowExpression',
                    'mdxJsxFlowElement',
                    'mdxJsxTextElement',
                    'mdxTextExpression',
                    'mdxjsEsm'
                  ]
                }
              ]
          ],
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
        //   editUrl:
        //     'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
        //   editUrl:
        //     'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        pages: {
            path: 'src/pages',
            routeBasePath: '',
            include: ['**/*.{js,jsx,ts,tsx,md,mdx}'],
            exclude: [
              '**/_*.{js,jsx,ts,tsx,md,mdx}',
              '**/_*/**',
              '**/*.test.{js,jsx,ts,tsx}',
              '**/__tests__/**',
            ],
            mdxPageComponent: '@theme/MDXPage',
            remarkPlugins: [
                remarkMath,
                [
                    remarkKroki,
                    {
                      server: 'https://kroki.io',
                      alias: ['mermaid','graphviz'],
                      target: 'mdx3',
                      output: 'img-html-base64'
                    }
                  ],
              ],
              rehypePlugins: [
                rehypeKatex,
                [
                    rehypeRaw,
                    {
                      passThrough: [
                        'mdxFlowExpression',
                        'mdxJsxFlowElement',
                        'mdxJsxTextElement',
                        'mdxTextExpression',
                        'mdxjsEsm'
                      ]
                    }
                  ]
              ],
            beforeDefaultRemarkPlugins: [],
            beforeDefaultRehypePlugins: [],
          },
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
       colorMode: {
           defaultMode: 'light',
           disableSwitch: true,
           respectPrefersColorScheme: false,
         },

         mermaid: {
            options: {
              maxTextSize: 999999,
            },
          },
      // Replace with your project's social card
      image: '/img/social-card.jpg',
      navbar: {
        title: '玩具帝国',
        logo: {
          alt: 'ToyEmpires Logo',
          src: '/img/icon.png',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'documentSidebar',
            position: 'left',
            label: '文档',
          },
          {
            to: '/download', 
            label: '下载', 
            position: 'left',
        },
        //   {
        //     href: 'https://github.com/facebook/docusaurus',
        //     label: 'GitHub',
        //     position: 'right',
        //   },
        ],
      },

      zoom: {
        selector: '.markdown :not(em) > img',
        config: {
          // options you can specify via https://github.com/francoischalifour/medium-zoom#usage
          background: {
            light: 'rgb(255, 255, 255)',
            dark: 'rgb(50, 50, 50)'
          }
        }
      },


      footer: {
        style: 'dark',
        // links: [
        //   {
        //     title: 'Docs',
        //     items: [
        //       {
        //         label: 'Tutorial',
        //         to: '/docs/intro',
        //       },
        //     ],
        //   },
        //   {
        //     title: 'Community',
        //     items: [
        //       {
        //         label: 'Stack Overflow',
        //         href: 'https://stackoverflow.com/questions/tagged/docusaurus',
        //       },
        //       {
        //         label: 'Discord',
        //         href: 'https://discordapp.com/invite/docusaurus',
        //       },
        //       {
        //         label: 'Twitter',
        //         href: 'https://twitter.com/docusaurus',
        //       },
        //     ],
        //   },
        //   {
        //     title: 'More',
        //     items: [
        //       {
        //         label: 'Blog',
        //         to: '/blog',
        //       },
        //       {
        //         label: 'GitHub',
        //         href: 'https://github.com/facebook/docusaurus',
        //       },
        //     ],
        //   },
        // ],
        copyright: `<div style="width:300px;margin:0 auto; padding:20px 0;">
        <img src="/img/beian.png" style="width:16px;">
      <a target="_blank" href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=44030502009931" style="display:inline-block;text-decoration:none;height:20px;line-height:20px;"><img src="" style="float:left;"/><p style="float:left;height:20px;line-height:20px;margin: 0px 0px 0px 5px; color:#939393;">粤公网安备 44030502009931号</p></a>
    </div>
    Copyright © ${new Date().getFullYear()} 二维公民, Inc. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),

    stylesheets: [
        {
          href: 'https://cdn.jsdelivr.net/npm/katex@0.13.24/dist/katex.min.css',
          type: 'text/css',
          integrity:
            'sha384-odtC+0UGzzFL/6PNoE8rX/SPcQDXBJ+uRepguP4QkPCm2LBxH3FA3y+fKSiJ+AmM',
          crossorigin: 'anonymous',
        },
      ],
      
};

export default config;
