/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    /**
     * Stylesheet generation mode.
     *
     * Set mode to "jit" if you want to generate your styles on-demand as you author your templates;
     * Set mode to "aot" if you want to generate the stylesheet in advance and purge later (aka legacy mode).
     */
    mode: "jit",
    // purge: [
    //     /**
    //      * HTML. Paths to Django template files that will contain Tailwind CSS classes.
    //      */
    //
    //     /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
    //     '../templates/**/*.html',
    //
    //     /*
    //      * Main templates directory of the project (BASE_DIR/templates).
    //      * Adjust the following line to match your project structure.
    //      */
    //     '../../templates/**/*.html',
    //
    //     /*
    //      * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
    //      * Adjust the following line to match your project structure.
    //      */
    //     '../../**/templates/**/*.html',
    //
    //     /**
    //      * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
    //      * patterns match your project structure.
    //      */
    //     /* JS 1: Ignore any JavaScript in node_modules folder. */
    //     // '!../../**/node_modules',
    //     /* JS 2: Process all JavaScript files in the project. */
    //     // '../../**/*.js',
    //
    //     /**
    //      * Python: If you use Tailwind CSS classes in Python, uncomment the following line
    //      * and make sure the pattern below matches your project structure.
    //      */
    //     '../../**/*.py'
    // ],
    purge: {
        enabled: true,
        content: [
            /**
             * HTML. Paths to Django template files that will contain Tailwind CSS classes.
             */

            /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
            '../templates/**/*.html',

            /*
             * Main templates directory of the project (BASE_DIR/templates).
             * Adjust the following line to match your project structure.
             */
            '../../templates/**/*.html',

            /*
             * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
             * Adjust the following line to match your project structure.
             */
            '../../**/templates/**/*.html',

            /**
             * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
             * patterns match your project structure.
             */
            /* JS 1: Ignore any JavaScript in node_modules folder. */
            // '!../../**/node_modules',
            /* JS 2: Process all JavaScript files in the project. */
            // '../../**/*.js',

            /**
             * Python: If you use Tailwind CSS classes in Python, uncomment the following line
             * and make sure the pattern below matches your project structure.
             */
            '../../**/*.py'
        ],
        safelist: [
            'min-w-screen',
            'w-screen',
            'min-h-screen',
            'h-screen'
        ]
    },
    darkMode: false, // or 'media' or 'class'
    theme: {
        extend: {
            colors: {
                gainsboro: '#DCDCDC',
                lifeinvader: {
                    DEFAULT: '#B60101'
                }
            },
            height: {
                '1/12': '8.333333%',
                '11/12': '91.666667%'
            },
            container: {
                center: true
            },
            fontFamily: {
                ubuntu: ['Ubuntu']
            }
        },
    },
    variants: {
        extend: {},
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
