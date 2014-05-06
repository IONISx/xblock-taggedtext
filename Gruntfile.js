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
                files: ['<%= c.static %>/js/src/**/*.js'],
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
                        '<%= c.static %>/js/src/**/*.js'
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
                    '<%= c.static %>/js/xblock-taggedtext.min.js': [
                        '<%= c.static %>/js/src/main.js',
                        '<%= c.static %>/js/src/studio.js'
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
