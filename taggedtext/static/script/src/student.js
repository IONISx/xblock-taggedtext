TaggedText.StudentView = function () {
    this.constructor.apply(this, arguments);
};

TaggedText.StudentView.prototype = {
    constructor: function (server, runtime, element) {
        this.runtime = runtime;
        this.server = server;
        this.element = $(element);

        this.state = this.element.find('.taggedtext').data('state') || {
            answers: []
        };
    },

    setupEvents: function () {
        var that = this;
        var keywords = this.element.find('.keyword');

        keywords.click(function () {
            $(this)
                .toggleClass('active')
                .find('.dropdown')
                .toggle();
            keywords.not(this).removeClass('active').find('.dropdown').hide();
        });

        $(document).click(function (e) {
            var activeKeyword = that.element.find('.keyword.active');

            if (!activeKeyword.is(e.target) && !activeKeyword.has(e.target).length)  {
                activeKeyword.removeClass('active').find('.dropdown').hide();
            }
        });

        this.element.find('.dropdown > li').click(function () {
            if (that.state.locked) {
                return false;
            }

            var el = $(this);
            var keyword = el.closest('.keyword');

            that.server.selectCategory({
                keyword: keyword.data('position'),
                category: el.data('id')
            }).done(function (data) {
                keyword.data('color', el.find('span').css('background-color'));

                that.state = data.state;
                that.refresh();
            }).fail(function () {
                // TODO: handle error
            });
        });

        this.element.find('.action .check').click(function () {
            if (that.state.locked) {
                return false;
            }

            that.server.check().done(function (data) {
                that.state = data.state;
                that.refresh();
            }).fail(function () {
                // TODO: handle error
            });
        });
    },

    _colorizeKeyword: function (keyword, answer) {
        keyword.toggleClass('graded', answer.graded);
        keyword.toggleClass('correct', answer.graded && answer.correct);
        keyword.toggleClass('incorrect', answer.graded && !answer.correct);

        if (answer.graded) {
            keyword.removeAttr('style').find('.dropdown').removeAttr('style');
        }
        else {
            var color = keyword.data('color');

            if (color) {
                keyword
                    .css({
                        'background-color': color,
                        'border-color': color
                    })
                    .find('.dropdown').css({
                        'border-color': color
                    });
            }
        }
    },

    _highlightAnswer: function (keyword, answer) {
        var categories = keyword.find('li');
        var selected = categories.filter(function () {
            return answer.answer === $(this).data('id');
        });

        categories.removeClass('active');
        selected.addClass('active');

        if (answer.real_answer) {
            var real = categories.filter(function () {
                return answer.real_answer === $(this).data('id');
            });

            categories.removeClass('real-answer');
            real.addClass('real-answer');
        }
    },

    _displayAttemptsInfo: function (attemptsInfo, state) {
        if (state.resolved) {
            if (state.attempts > 1) {
                attemptsInfo.text('Bravo ! Vous avez résolu le problème en ' + state.attempts + ' essais.');
            }
            else {
                attemptsInfo.text('Bravo ! Vous avez résolu le problème en un seul essai.');
            }
        }
        else if (state.max_attempts) {
            var remain = state.max_attempts - state.attempts;
            if (remain > 1) {
                attemptsInfo.text('Il vous reste ' + remain + ' essais !');
            }
            else if (remain > 0) {
                if (state.max_attempts === 1) {
                    attemptsInfo.text('Attention, vous n’avez qu’un seul essai !');
                }
                else {
                    attemptsInfo.text('Attention, il ne vous reste qu’un essai !');
                }
            }
            else {
                if (state.max_attempts > 1) {
                    attemptsInfo.text('Vous avez épuisé vos ' + state.max_attempts + ' essais…');
                }
                else {
                    attemptsInfo.text('Vous n’aviez qu’un seul essai, dommage…');
                }
            }
        }
    },

    _updateProgress: function (tab, progress) {
        var prefix = 'progress-';
        var classes = tab.attr('class').split(' ').filter(function(c) {
            return c.lastIndexOf(prefix, 0) !== 0;
        });
        tab.attr('class', classes.join(' '));
        tab.addClass(prefix + progress.status);
    },

    _updateScore: function (el, progress) {
        el.text('(' + progress.detail + ' points)');
    },

    refresh: function () {
        var that = this;

        this.element.find('.attempts').text(this.state.attempts);

        var categories = this.element.find('.categories .category');
        categories.each(function () {
            var category = $(this);
            var id = category.data('id');

            category.find('.count').text(that.state.counts[id] || 0);
        });

        var keywords = this.element.find('.text .keyword');
        keywords.toggleClass('locked', this.state.locked);
        keywords.each(function () {
            var keyword = $(this);
            var position = keyword.data('position');

            var answer = $.grep(that.state.answers, function (a) {
                return a.position === position;
            });

            if (answer.length) {
                answer = answer[0];

                that._colorizeKeyword(keyword, answer);
                that._highlightAnswer(keyword, answer);
            }
        });

        this.element.find('input.check').toggleClass('disabled', this.state.locked);

        this._displayAttemptsInfo(this.element.find('.submission_feedback'), this.state);

        if (this.state.progress) {
            this._updateProgress($('#sequence-list').find('a.active'), this.state.progress);
            this._updateScore(this.element.find('.problem-progress'), this.state.progress);
        }
    },

    render: function () {
        this.setupEvents();
        this.refresh();
    }
};
