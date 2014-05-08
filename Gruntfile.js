'use strict';

module.exports = function (grunt) {
    require('matchdep').filterDev('grunt-*').forEach(grunt.loadNpmTasks);

    var config = {
        'code': 'taggedtext',
        'static': 'taggedtext/static'
    };

    grunt.initConfig({
        c: config,

        // ## //

        watch: {
            uglify: {
                files: ['<%= c.static %>/script/src/**/*.js'],
                tasks: ['uglify']
            },
            less: {
                files: ['<%= c.static %>/style/src/**/*.less'],
                tasks: ['less', 'cssmin']
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
                        'TaggedText': true
                    }
                }
            },
            node: {
                files: {
                    src: [
                        'Gruntfile.js'
                    ]
                },
                options: {
                    'node': true
                }
            }
        },

        // ## //

        flake8: {
            python: {
                options: {
                    maxLineLength: 120,
                    hangClosing: false
                },
                src: [
                    'setup.py',
                    '<%= c.code %>/**/*.py'
                ]
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
                        '<%= c.static %>/script/src/server.js',
                        '<%= c.static %>/script/src/studio.js',
                        '<%= c.static %>/script/src/student.js',
                        '<%= c.static %>/script/src/xblock.js'
                    ]
                }
            }
        },

        // ## //

        less: {
            style: {
                files: {
                    '<%= c.static %>/style/xblock-taggedtext.min.css': '<%= c.static %>/style/src/main.less'
                }
            }
        },

        // ## //

        cssmin: {
            style: {
                options: {
                    report: 'min'
                },
                files: {
                    '<%= c.static %>/style/xblock-taggedtext.min.css': '<%= c.static %>/style/xblock-taggedtext.min.css'
                }
            }
        }
    });

    grunt.registerTask('build', [
        'uglify',
        'less',
        'cssmin'
    ]);

    grunt.registerTask('default', function () {
        grunt.option('force', true);

        grunt.task.run([
            'build',
            'watch'
        ]);
    });

    grunt.registerTask('test', [
        'jshint',
        'flake8',
        'build'
    ]);
};
