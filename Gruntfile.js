'use strict';

module.exports = function (grunt) {
    require('matchdep').filterDev('grunt-*').forEach(grunt.loadNpmTasks);

    var config = {
        'static': 'taggedtext/static',
        bower: 'bower_components'
    };

    grunt.initConfig({
        c: config,

        // ## //

        watch: {
            uglify: {
                files: ['<%= c.static %>/script/src/**/*.js'],
                tasks: ['uglify']
            }
        },

        // ## //

        jshint: {
            options: {
                'curly': true,
                'eqeqeq': true,
                'immed': true,
                'latedef': true,
                'newcap': true,
                'noarg': true,
                'noempty': true,
                'unused': true,
                'undef': true,
                'trailing': true,
                'quotmark': 'single',

                'boss': true,
                'eqnull': true
            },
            browser: {
                files: {
                    src: [
                        '<%= c.static %>/script/src/**/*.js'
                    ]
                },
                options: {
                    'browser': true,
                    'jquery': true,
                    'globals': {
                        'CodeMirror': true,
                        'TaggedTextXBlock': true
                    }
                }
            }
        },

        // ## //

        uglify: {
            script: {
                options: {
                    report: 'min'
                },
                files: {
                    '<%= c.static %>/script/xblock-taggedtext.min.js': [
                        '<%= c.static %>/script/src/main.js',
                        '<%= c.static %>/script/src/studio.js',
                        '<%= c.static %>/script/src/xblock.js'
                    ]
                }
            }
        }
    });

    grunt.registerTask('default', function () {
        grunt.option('force', true);

        grunt.task.run([
            'uglify',
            'watch'
        ]);
    });

    grunt.registerTask('build', [
        'jshint:browser',
        'uglify'
    ]);
};
