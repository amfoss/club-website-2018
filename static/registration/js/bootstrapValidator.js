/**
 * BootstrapValidator (http://bootstrapvalidator.com)
 * The best jQuery plugin to validate form fields. Designed to use with Bootstrap 3
 *
 * @author      https://twitter.com/nghuuphuoc
 * @copyright   (c) 2013 - 2014 Nguyen Huu Phuoc
 * @license     Commercial: http://bootstrapvalidator.com/license/
 *              Non-commercial: http://creativecommons.org/licenses/by-nc-nd/3.0/
 */

if (typeof jQuery === 'undefined') {
    throw new Error('BootstrapValidator requires jQuery');
}

(function($) {
    var version = $.fn.jquery.split(' ')[0].split('.');
    if ((+version[0] < 2 && +version[1] < 9) || (+version[0] === 1 && +version[1] === 9 && +version[2] < 1)) {
        throw new Error('BootstrapValidator requires jQuery version 1.9.1 or higher');
    }
}(window.jQuery));

(function($) {
    var BootstrapValidator = function(form, options) {
        this.$form   = $(form);
        this.options = $.extend({}, $.fn.bootstrapValidator.DEFAULT_OPTIONS, options);

        this.$invalidFields = $([]);    // Array of invalid fields
        this.$submitButton  = null;     // The submit button which is clicked to submit form
        this.$hiddenButton  = null;

        // Validating status
        this.STATUS_NOT_VALIDATED = 'NOT_VALIDATED';
        this.STATUS_VALIDATING    = 'VALIDATING';
        this.STATUS_INVALID       = 'INVALID';
        this.STATUS_VALID         = 'VALID';

        // Determine the event that is fired when user change the field value
        // Most modern browsers supports input event except IE 7, 8.
        // IE 9 supports input event but the event is still not fired if I press the backspace key.
        // Get IE version
        // https://gist.github.com/padolsey/527683/#comment-7595
        var ieVersion = (function() {
            var v = 3, div = document.createElement('div'), a = div.all || [];
            while (div.innerHTML = '<!--[if gt IE '+(++v)+']><br><![endif]-->', a[0]) {}
            return v > 4 ? v : !v;
        }());

        var el = document.createElement('div');
        this._changeEvent = (ieVersion === 9 || !('oninput' in el)) ? 'keyup' : 'input';

        // The flag to indicate that the form is ready to submit when a remote/callback validator returns
        this._submitIfValid = null;

        // Field elements
        this._cacheFields = {};

        this._init();
    };

    BootstrapValidator.prototype = {
        constructor: BootstrapValidator,

        /**
         * Init form
         */
        _init: function() {
            var that    = this,
                options = {
                    autoFocus:      this.$form.attr('data-bv-autofocus'),
                    container:      this.$form.attr('data-bv-container'),
                    events: {
                        formInit:         this.$form.attr('data-bv-events-form-init'),
                        formError:        this.$form.attr('data-bv-events-form-error'),
                        formSuccess:      this.$form.attr('data-bv-events-form-success'),
                        fieldAdded:       this.$form.attr('data-bv-events-field-added'),
                        fieldRemoved:     this.$form.attr('data-bv-events-field-removed'),
                        fieldInit:        this.$form.attr('data-bv-events-field-init'),
                        fieldError:       this.$form.attr('data-bv-events-field-error'),
                        fieldSuccess:     this.$form.attr('data-bv-events-field-success'),
                        fieldStatus:      this.$form.attr('data-bv-events-field-status'),
                        validatorError:   this.$form.attr('data-bv-events-validator-error'),
                        validatorSuccess: this.$form.attr('data-bv-events-validator-success')
                    },
                    excluded:       this.$form.attr('data-bv-excluded'),
                    feedbackIcons: {
                        valid:      this.$form.attr('data-bv-feedbackicons-valid'),
                        invalid:    this.$form.attr('data-bv-feedbackicons-invalid'),
                        validating: this.$form.attr('data-bv-feedbackicons-validating')
                    },
                    group:          this.$form.attr('data-bv-group'),
                    live:           this.$form.attr('data-bv-live'),
                    message:        this.$form.attr('data-bv-message'),
                    onError:        this.$form.attr('data-bv-onerror'),
                    onSuccess:      this.$form.attr('data-bv-onsuccess'),
                    submitButtons:  this.$form.attr('data-bv-submitbuttons'),
                    threshold:      this.$form.attr('data-bv-threshold'),
                    trigger:        this.$form.attr('data-bv-trigger'),
                    verbose:        this.$form.attr('data-bv-verbose'),
                    fields:         {}
                };

            this.$form
                // Disable client side validation in HTML 5
                .attr('novalidate', 'novalidate')
                .addClass(this.options.elementClass)
                // Disable the default submission first
                .on('submit.bv', function(e) {
                    e.preventDefault();
                    that.validate();
                })
                .on('click.bv', this.options.submitButtons, function() {
                    that.$submitButton  = $(this);
					// The user just click the submit button
					that._submitIfValid = true;
                })
                // Find all fields which have either "name" or "data-bv-field" attribute
                .find('[name], [data-bv-field]')
                    .each(function() {
                        var $field = $(this),
                            field  = $field.attr('name') || $field.attr('data-bv-field'),
                            opts   = that._parseOptions($field);
                        if (opts) {
                            $field.attr('data-bv-field', field);
                            options.fields[field] = $.extend({}, opts, options.fields[field]);
                        }
                    });

            this.options = $.extend(true, this.options, options);

            // When pressing Enter on any field in the form, the first submit button will do its job.
            // The form then will be submitted.
            // I create a first hidden submit button
            this.$hiddenButton = $('<button/>')
                                    .attr('type', 'submit')
                                    .prependTo(this.$form)
                                    .addClass('bv-hidden-submit')
                                    .css({ display: 'none', width: 0, height: 0 });

            this.$form
                .on('click.bv', '[type="submit"]', function(e) {
                    // #746: Check if the button click handler returns false
                    if (!e.isDefaultPrevented()) {
                        var $target = $(e.target),
                            // The button might contain HTML tag
                            $button = $target.is('[type="submit"]') ? $target.eq(0) : $target.parent('[type="submit"]').eq(0);

                        // Don't perform validation when clicking on the submit button/input
                        // which aren't defined by the 'submitButtons' option
                        if (that.options.submitButtons && !$button.is(that.options.submitButtons) && !$button.is(that.$hiddenButton)) {
                            that.$form.off('submit.bv').submit();
                        }
                    }
                });

            for (var field in this.options.fields) {
                this._initField(field);
            }

            this.$form.trigger($.Event(this.options.events.formInit), {
                bv: this,
                options: this.options
            });

            // Prepare the events
            if (this.options.onSuccess) {
                this.$form.on(this.options.events.formSuccess, function(e) {
                    $.fn.bootstrapValidator.helpers.call(that.options.onSuccess, [e]);
                });
            }
            if (this.options.onError) {
                this.$form.on(this.options.events.formError, function(e) {
                    $.fn.bootstrapValidator.helpers.call(that.options.onError, [e]);
                });
            }
        },

        /**
         * Parse the validator options from HTML attributes
         *
         * @param {jQuery} $field The field element
         * @returns {Object}
         */
        _parseOptions: function($field) {
            var field      = $field.attr('name') || $field.attr('data-bv-field'),
                validators = {},
                validator,
                v,          // Validator name
                attrName,
                enabled,
                optionName,
                optionAttrName,
                optionValue,
                html5AttrName,
                html5AttrMap;

            for (v in $.fn.bootstrapValidator.validators) {
                validator    = $.fn.bootstrapValidator.validators[v];
                attrName     = 'data-bv-' + v.toLowerCase(),
                enabled      = $field.attr(attrName) + '';
                html5AttrMap = ('function' === typeof validator.enableByHtml5) ? validator.enableByHtml5($field) : null;

                if ((html5AttrMap && enabled !== 'false')
                    || (html5AttrMap !== true && ('' === enabled || 'true' === enabled || attrName === enabled.toLowerCase())))
                {
                    // Try to parse the options via attributes
                    validator.html5Attributes = $.extend({}, { message: 'message', onerror: 'onError', onsuccess: 'onSuccess' }, validator.html5Attributes);
                    validators[v] = $.extend({}, html5AttrMap === true ? {} : html5AttrMap, validators[v]);

                    for (html5AttrName in validator.html5Attributes) {
                        optionName  = validator.html5Attributes[html5AttrName];
                        optionAttrName = 'data-bv-' + v.toLowerCase() + '-' + html5AttrName,
                        optionValue = $field.attr(optionAttrName);
                        if (optionValue) {
                            if ('true' === optionValue || optionAttrName === optionValue.toLowerCase()) {
                                optionValue = true;
                            } else if ('false' === optionValue) {
                                optionValue = false;
                            }
                            validators[v][optionName] = optionValue;
                        }
                    }
                }
            }

            var opts = {
                    autoFocus:     $field.attr('data-bv-autofocus'),
                    container:     $field.attr('data-bv-container'),
                    excluded:      $field.attr('data-bv-excluded'),
                    feedbackIcons: $field.attr('data-bv-feedbackicons'),
                    group:         $field.attr('data-bv-group'),
                    message:       $field.attr('data-bv-message'),
                    onError:       $field.attr('data-bv-onerror'),
                    onStatus:      $field.attr('data-bv-onstatus'),
                    onSuccess:     $field.attr('data-bv-onsuccess'),
                    selector:      $field.attr('data-bv-selector'),
                    threshold:     $field.attr('data-bv-threshold'),
                    trigger:       $field.attr('data-bv-trigger'),
                    verbose:       $field.attr('data-bv-verbose'),
                    validators:    validators
                },
                emptyOptions    = $.isEmptyObject(opts),        // Check if the field options are set using HTML attributes
                emptyValidators = $.isEmptyObject(validators);  // Check if the field validators are set using HTML attributes

            if (!emptyValidators || (!emptyOptions && this.options.fields && this.options.fields[field])) {
                opts.validators = validators;
                return opts;
            } else {
                return null;
            }
        },

        /**
         * Init field
         *
         * @param {String|jQuery} field The field name or field element
         */
        _initField: function(field) {
            var fields = $([]);
            switch (typeof field) {
                case 'object':
                    fields = field;
                    field  = field.attr('data-bv-field');
                    break;
                case 'string':
                    fields = this.getFieldElements(field);
                    fields.attr('data-bv-field', field);
                    break;
                default:
                    break;
            }

            // We don't need to validate non-existing fields
            if (fields.length === 0) {
                return;
            }

            if (this.options.fields[field] === null || this.options.fields[field].validators === null) {
                return;
            }

            var validatorName;
            for (validatorName in this.options.fields[field].validators) {
                if (!$.fn.bootstrapValidator.validators[validatorName]) {
                    delete this.options.fields[field].validators[validatorName];
                }
            }
            if (this.options.fields[field].enabled === null) {
                this.options.fields[field].enabled = true;
            }

            var that      = this,
                total     = fields.length,
                type      = fields.attr('type'),
                updateAll = (total === 1) || ('radio' === type) || ('checkbox' === type),
                event     = ('radio' === type || 'checkbox' === type || 'file' === type || 'SELECT' === fields.eq(0).get(0).tagName) ? 'change' : this._changeEvent,
                trigger   = (this.options.fields[field].trigger || this.options.trigger || event).split(' '),
                events    = $.map(trigger, function(item) {
                    return item + '.update.bv';
                }).join(' ');

            for (var i = 0; i < total; i++) {
                var $field    = fields.eq(i),
                    group     = this.options.fields[field].group || this.options.group,
                    $parent   = $field.parents(group),
                    // Allow user to indicate where the error messages are shown
                    container = ('function' === typeof (this.options.fields[field].container || this.options.container)) ? (this.options.fields[field].container || this.options.container).call(this, $field, this) : (this.options.fields[field].container || this.options.container),
                    $message  = (container && container !== 'tooltip' && container !== 'popover') ? $(container) : this._getMessageContainer($field, group);

                if (container && container !== 'tooltip' && container !== 'popover') {
                    $message.addClass('has-error');
                }

                // Remove all error messages and feedback icons
                $message.find('.help-block[data-bv-validator][data-bv-for="' + field + '"]').remove();
                $parent.find('i[data-bv-icon-for="' + field + '"]').remove();

                // Whenever the user change the field value, mark it as not validated yet
                $field.off(events).on(events, function() {
                    that.updateStatus($(this), that.STATUS_NOT_VALIDATED);
                });
                
                // Create help block elements for showing the error messages
                $field.data('bv.messages', $message);
                for (validatorName in this.options.fields[field].validators) {
                    $field.data('bv.result.' + validatorName, this.STATUS_NOT_VALIDATED);

                    if (!updateAll || i === total - 1) {
                        $('<small/>')
                            .css('display', 'none')
                            .addClass('help-block')
                            .attr('data-bv-validator', validatorName)
                            .attr('data-bv-for', field)
                            .attr('data-bv-result', this.STATUS_NOT_VALIDATED)
                            .html(this._getMessage(field, validatorName))
                            .appendTo($message);
                    }

                    // Init the validator
                    if ('function' === typeof $.fn.bootstrapValidator.validators[validatorName].init) {
                        $.fn.bootstrapValidator.validators[validatorName].init(this, $field, this.options.fields[field].validators[validatorName]);
                    }
                }

                // Prepare the feedback icons
                // Available from Bootstrap 3.1 (http://getbootstrap.com/css/#forms-control-validation)
                if (this.options.fields[field].feedbackIcons !== false && this.options.fields[field].feedbackIcons !== 'false'
                    && this.options.feedbackIcons
                    && this.options.feedbackIcons.validating && this.options.feedbackIcons.invalid && this.options.feedbackIcons.valid
                    && (!updateAll || i === total - 1))
                {
                    // $parent.removeClass('has-success').removeClass('has-error').addClass('has-feedback');
                    // Keep error messages which are populated from back-end
                    $parent.addClass('has-feedback');
                    var $icon = $('<i/>')
                                    .css('display', 'none')
                                    .addClass('form-control-feedback')
                                    .attr('data-bv-icon-for', field)
                                    .insertAfter($field);

                    // Place it after the container of checkbox/radio
                    // so when clicking the icon, it doesn't effect to the checkbox/radio element
                    if ('checkbox' === type || 'radio' === type) {
                        var $fieldParent = $field.parent();
                        if ($fieldParent.hasClass(type)) {
                            $icon.insertAfter($fieldParent);
                        } else if ($fieldParent.parent().hasClass(type)) {
                            $icon.insertAfter($fieldParent.parent());
                        }
                    }

                    // The feedback icon does not render correctly if there is no label
                    // https://github.com/twbs/bootstrap/issues/12873
                    if ($parent.find('label').length === 0) {
                        $icon.addClass('bv-no-label');
                    }
                    // Fix feedback icons in input-group
                    if ($parent.find('.input-group').length !== 0) {
                        $icon.addClass('bv-icon-input-group')
                             .insertAfter($parent.find('.input-group').eq(0));
                    }

                    // Store the icon as a data of field element
                    if (!updateAll) {
                        $field.data('bv.icon', $icon);
                    } else if (i === total - 1) {
                        // All fields with the same name have the same icon
                        fields.data('bv.icon', $icon);
                    }
                    
                    if (container) {
                        $field
                            // Show tooltip/popover message when field gets focus
                            .off('focus.container.bv')
                            .on('focus.container.bv', function() {
                                switch (container) {
                                    case 'tooltip':
                                        $(this).data('bv.icon').tooltip('show');
                                        break;
                                    case 'popover':
                                        $(this).data('bv.icon').popover('show');
                                        break;
                                    default:
                                        break;
                                }
                            })
                            // and hide them when losing focus
                            .off('blur.container.bv')
                            .on('blur.container.bv', function() {
                                switch (container) {
                                    case 'tooltip':
                                        $(this).data('bv.icon').tooltip('hide');
                                        break;
                                    case 'popover':
                                        $(this).data('bv.icon').popover('hide');
                                        break;
                                    default:
                                        break;
                                }
                            });
                    }
                }
            }

            // Prepare the events
            fields
                .on(this.options.events.fieldSuccess, function(e, data) {
                    var onSuccess = that.getOptions(data.field, null, 'onSuccess');
                    if (onSuccess) {
                        $.fn.bootstrapValidator.helpers.call(onSuccess, [e, data]);
                    }
                })
                .on(this.options.events.fieldError, function(e, data) {
                    var onError = that.getOptions(data.field, null, 'onError');
                    if (onError) {
                        $.fn.bootstrapValidator.helpers.call(onError, [e, data]);
                    }
                })
                .on(this.options.events.fieldStatus, function(e, data) {
                    var onStatus = that.getOptions(data.field, null, 'onStatus');
                    if (onStatus) {
                        $.fn.bootstrapValidator.helpers.call(onStatus, [e, data]);
                    }
                })
                .on(this.options.events.validatorError, function(e, data) {
                    var onError = that.getOptions(data.field, data.validator, 'onError');
                    if (onError) {
                        $.fn.bootstrapValidator.helpers.call(onError, [e, data]);
                    }
                })
                .on(this.options.events.validatorSuccess, function(e, data) {
                    var onSuccess = that.getOptions(data.field, data.validator, 'onSuccess');
                    if (onSuccess) {
                        $.fn.bootstrapValidator.helpers.call(onSuccess, [e, data]);
                    }
                });

            // Set live mode
            events = $.map(trigger, function(item) {
                return item + '.live.bv';
            }).join(' ');
            switch (this.options.live) {
                case 'submitted':
                    break;
                case 'disabled':
                    fields.off(events);
                    break;
                case 'enabled':
                /* falls through */
                default:
                    fields.off(events).on(events, function() {
                        if (that._exceedThreshold($(this))) {
                            that.validateField($(this));
                        }
                    });
                    break;
            }

            fields.trigger($.Event(this.options.events.fieldInit), {
                bv: this,
                field: field,
                element: fields
            });
        },

        /**
         * Get the error message for given field and validator
         *
         * @param {String} field The field name
         * @param {String} validatorName The validator name
         * @returns {String}
         */
        _getMessage: function(field, validatorName) {
            if (!this.options.fields[field] || !$.fn.bootstrapValidator.validators[validatorName]
                || !this.options.fields[field].validators || !this.options.fields[field].validators[validatorName])
            {
                return '';
            }

            var options = this.options.fields[field].validators[validatorName];
            switch (true) {
                case (!!options.message):
                    return options.message;
                case (!!this.options.fields[field].message):
                    return this.options.fields[field].message;
                case (!!$.fn.bootstrapValidator.i18n[validatorName]):
                    return $.fn.bootstrapValidator.i18n[validatorName]['default'];
                default:
                    return this.options.message;
            }
        },

        /**
         * Get the element to place the error messages
         *
         * @param {jQuery} $field The field element
         * @param {String} group
         * @returns {jQuery}
         */
        _getMessageContainer: function($field, group) {
            var $parent = $field.parent();
            if ($parent.is(group)) {
                return $parent;
            }

            var cssClasses = $parent.attr('class');
            if (!cssClasses) {
                return this._getMessageContainer($parent, group);
            }

            cssClasses = cssClasses.split(' ');
            var n = cssClasses.length;
            for (var i = 0; i < n; i++) {
                if (/^col-(xs|sm|md|lg)-\d+$/.test(cssClasses[i]) || /^col-(xs|sm|md|lg)-offset-\d+$/.test(cssClasses[i])) {
                    return $parent;
                }
            }

            return this._getMessageContainer($parent, group);
        },

        /**
         * Called when all validations are completed
         */
        _submit: function() {
            var isValid   = this.isValid(),
                eventType = isValid ? this.options.events.formSuccess : this.options.events.formError,
                e         = $.Event(eventType);

            this.$form.trigger(e);

            // Call default handler
            // Check if whether the submit button is clicked
            if (this.$submitButton) {
                isValid ? this._onSuccess(e) : this._onError(e);
            }
        },

        /**
         * Check if the field is excluded.
         * Returning true means that the field will not be validated
         *
         * @param {jQuery} $field The field element
         * @returns {Boolean}
         */
        _isExcluded: function($field) {
            var excludedAttr = $field.attr('data-bv-excluded'),
                // I still need to check the 'name' attribute while initializing the field
                field        = $field.attr('data-bv-field') || $field.attr('name');

            switch (true) {
                case (!!field && this.options.fields && this.options.fields[field] && (this.options.fields[field].excluded === 'true' || this.options.fields[field].excluded === true)):
                case (excludedAttr === 'true'):
                case (excludedAttr === ''):
                    return true;

                case (!!field && this.options.fields && this.options.fields[field] && (this.options.fields[field].excluded === 'false' || this.options.fields[field].excluded === false)):
                case (excludedAttr === 'false'):
                    return false;

                default:
                    if (this.options.excluded) {
                        // Convert to array first
                        if ('string' === typeof this.options.excluded) {
                            this.options.excluded = $.map(this.options.excluded.split(','), function(item) {
                                // Trim the spaces
                                return $.trim(item);
                            });
                        }

                        var length = this.options.excluded.length;
                        for (var i = 0; i < length; i++) {
                            if (('string' === typeof this.options.excluded[i] && $field.is(this.options.excluded[i]))
                                || ('function' === typeof this.options.excluded[i] && this.options.excluded[i].call(this, $field, this) === true))
                            {
                                return true;
                            }
                        }
                    }
                    return false;
            }
        },

        /**
         * Check if the number of characters of field value exceed the threshold or not
         *
         * @param {jQuery} $field The field element
         * @returns {Boolean}
         */
        _exceedThreshold: function($field) {
            var field     = $field.attr('data-bv-field'),
                threshold = this.options.fields[field].threshold || this.options.threshold;
            if (!threshold) {
                return true;
            }
            var cannotType = $.inArray($field.attr('type'), ['button', 'checkbox', 'file', 'hidden', 'image', 'radio', 'reset', 'submit']) !== -1;
            return (cannotType || $field.val().length >= threshold);
        },
        
        // ---
        // Events
        // ---

        /**
         * The default handler of error.form.bv event.
         * It will be called when there is a invalid field
         *
         * @param {jQuery.Event} e The jQuery event object
         */
        _onError: function(e) {
            if (e.isDefaultPrevented()) {
                return;
            }

            if ('submitted' === this.options.live) {
                // Enable live mode
                this.options.live = 'enabled';
                var that = this;
                for (var field in this.options.fields) {
                    (function(f) {
                        var fields  = that.getFieldElements(f);
                        if (fields.length) {
                            var type    = $(fields[0]).attr('type'),
                                event   = ('radio' === type || 'checkbox' === type || 'file' === type || 'SELECT' === $(fields[0]).get(0).tagName) ? 'change' : that._changeEvent,
                                trigger = that.options.fields[field].trigger || that.options.trigger || event,
                                events  = $.map(trigger.split(' '), function(item) {
                                    return item + '.live.bv';
                                }).join(' ');

                            fields.off(events).on(events, function() {
                                if (that._exceedThreshold($(this))) {
                                    that.validateField($(this));
                                }
                            });
                        }
                    })(field);
                }
            }

            // Determined the first invalid field which will be focused on automatically
            for (var i = 0; i < this.$invalidFields.length; i++) {
                var $field    = this.$invalidFields.eq(i),
                    autoFocus = this._isOptionEnabled($field.attr('data-bv-field'), 'autoFocus');
                if (autoFocus) {
                    // Activate the tab containing the field if exists
                    var $tabPane = $field.parents('.tab-pane'), tabId;
                    if ($tabPane && (tabId = $tabPane.attr('id'))) {
                        $('a[href="#' + tabId + '"][data-toggle="tab"]').tab('show');
                    }

                    // Focus the field
                    $field.focus();
                    break;
                }
            }
        },

        /**
         * The default handler of success.form.bv event.
         * It will be called when all the fields are valid
         *
         * @param {jQuery.Event} e The jQuery event object
         */
        _onSuccess: function(e) {
            if (e.isDefaultPrevented()) {
                return;
            }

            // Submit the form
            this.disableSubmitButtons(true).defaultSubmit();
        },

        /**
         * Called after validating a field element
         *
         * @param {jQuery} $field The field element
         * @param {String} [validatorName] The validator name
         */
        _onFieldValidated: function($field, validatorName) {
            var field         = $field.attr('data-bv-field'),
                validators    = this.options.fields[field].validators,
                counter       = {},
                numValidators = 0,
                data          = {
                    bv: this,
                    field: field,
                    element: $field,
                    validator: validatorName,
                    result: $field.data('bv.response.' + validatorName)
                };

            // Trigger an event after given validator completes
            if (validatorName) {
                switch ($field.data('bv.result.' + validatorName)) {
                    case this.STATUS_INVALID:
                        $field.trigger($.Event(this.options.events.validatorError), data);
                        break;
                    case this.STATUS_VALID:
                        $field.trigger($.Event(this.options.events.validatorSuccess), data);
                        break;
                    default:
                        break;
                }
            }

            counter[this.STATUS_NOT_VALIDATED] = 0;
            counter[this.STATUS_VALIDATING]    = 0;
            counter[this.STATUS_INVALID]       = 0;
            counter[this.STATUS_VALID]         = 0;

            for (var v in validators) {
                if (validators[v].enabled === false) {
                    continue;
                }

                numValidators++;
                var result = $field.data('bv.result.' + v);
                if (result) {
                    counter[result]++;
                }
            }

            if (counter[this.STATUS_VALID] === numValidators) {
                // Remove from the list of invalid fields
                this.$invalidFields = this.$invalidFields.not($field);

                $field.trigger($.Event(this.options.events.fieldSuccess), data);
            }
            // If all validators are completed and there is at least one validator which doesn't pass
            else if ((counter[this.STATUS_NOT_VALIDATED] === 0 || !this._isOptionEnabled(field, 'verbose')) && counter[this.STATUS_VALIDATING] === 0 && counter[this.STATUS_INVALID] > 0) {
                // Add to the list of invalid fields
                this.$invalidFields = this.$invalidFields.add($field);

                $field.trigger($.Event(this.options.events.fieldError), data);
            }
        },

        /**
         * Check whether or not a field option is enabled
         *
         * @param {String} field The field name
         * @param {String} option The option name, "verbose", "autoFocus", for example
         * @returns {Boolean}
         */
        _isOptionEnabled: function(field, option) {
            if (this.options.fields[field] && (this.options.fields[field][option] === 'true' || this.options.fields[field][option] === true)) {
                return true;
            }
            if (this.options.fields[field] && (this.options.fields[field][option] === 'false' || this.options.fields[field][option] === false)) {
                return false;
            }
            return this.options[option] === 'true' || this.options[option] === true;
        },

        // ---
        // Public methods
        // ---

        /**
         * Retrieve the field elements by given name
         *
         * @param {String} field The field name
         * @returns {null|jQuery[]}
         */
        getFieldElements: function(field) {
            if (!this._cacheFields[field]) {
                this._cacheFields[field] = (this.options.fields[field] && this.options.fields[field].selector)
                                         ? $(this.options.fields[field].selector)
                                         : this.$form.find('[name="' + field + '"]');
            }

            return this._cacheFields[field];
        },

        /**
         * Get the field options
         *
         * @param {String|jQuery} [field] The field name or field element. If it is not set, the method returns the form options
         * @param {String} [validator] The name of validator. It null, the method returns form options
         * @param {String} [option] The option name
         * @return {String|Object}
         */
        getOptions: function(field, validator, option) {
            if (!field) {
                return option ? this.options[option] : this.options;
            }
            if ('object' === typeof field) {
                field = field.attr('data-bv-field');
            }
            if (!this.options.fields[field]) {
                return null;
            }

            var options = this.options.fields[field];
            if (!validator) {
                return option ? options[option] : options;
            }
            if (!options.validators || !options.validators[validator]) {
                return null;
            }

            return option ? options.validators[validator][option] : options.validators[validator];
        },

        /**
         * Disable/enable submit buttons
         *
         * @param {Boolean} disabled Can be true or false
         * @returns {BootstrapValidator}
         */
        disableSubmitButtons: function(disabled) {
            if (!disabled) {
                this.$form.find(this.options.submitButtons).removeAttr('disabled');
            } else if (this.options.live !== 'disabled') {
                // Don't disable if the live validating mode is disabled
                this.$form.find(this.options.submitButtons).attr('disabled', 'disabled');
            }

            return this;
        },

        /**
         * Validate the form
         *
         * @returns {BootstrapValidator}
         */
        validate: function() {
            if (!this.options.fields) {
                return this;
            }
            this.disableSubmitButtons(true);

            this._submitIfValid = false;
            for (var field in this.options.fields) {
                this.validateField(field);
            }

            this._submit();
            this._submitIfValid = true;

            return this;
        },

        /**
         * Validate given field
         *
         * @param {String|jQuery} field The field name or field element
         * @returns {BootstrapValidator}
         */
        validateField: function(field) {
            var fields = $([]);
            switch (typeof field) {
                case 'object':
                    fields = field;
                    field  = field.attr('data-bv-field');
                    break;
                case 'string':
                    fields = this.getFieldElements(field);
                    break;
                default:
                    break;
            }

            if (fields.length === 0 || !this.options.fields[field] || this.options.fields[field].enabled === false) {
                return this;
            }

            var that       = this,
                type       = fields.attr('type'),
                total      = ('radio' === type || 'checkbox' === type) ? 1 : fields.length,
                updateAll  = ('radio' === type || 'checkbox' === type),
                validators = this.options.fields[field].validators,
                verbose    = this._isOptionEnabled(field, 'verbose'),
                validatorName,
                validateResult;

            for (var i = 0; i < total; i++) {
                var $field = fields.eq(i);
                if (this._isExcluded($field)) {
                    continue;
                }

                var stop = false;
                for (validatorName in validators) {
                    if ($field.data('bv.dfs.' + validatorName)) {
                        $field.data('bv.dfs.' + validatorName).reject();
                    }
                    if (stop) {
                        break;
                    }

                    // Don't validate field if it is already done
                    var result = $field.data('bv.result.' + validatorName);
                    if (result === this.STATUS_VALID || result === this.STATUS_INVALID) {
                        this._onFieldValidated($field, validatorName);
                        continue;
                    } else if (validators[validatorName].enabled === false) {
                        this.updateStatus(updateAll ? field : $field, this.STATUS_VALID, validatorName);
                        continue;
                    }

                    $field.data('bv.result.' + validatorName, this.STATUS_VALIDATING);
                    validateResult = $.fn.bootstrapValidator.validators[validatorName].validate(this, $field, validators[validatorName]);

                    // validateResult can be a $.Deferred object ...
                    if ('object' === typeof validateResult && validateResult.resolve) {
                        this.updateStatus(updateAll ? field : $field, this.STATUS_VALIDATING, validatorName);
                        $field.data('bv.dfs.' + validatorName, validateResult);

                        validateResult.done(function($f, v, response) {
                            // v is validator name
                            $f.removeData('bv.dfs.' + v).data('bv.response.' + v, response);
                            if (response.message) {
                                that.updateMessage($f, v, response.message);
                            }

                            that.updateStatus(updateAll ? $f.attr('data-bv-field') : $f, response.valid ? that.STATUS_VALID : that.STATUS_INVALID, v);

                            if (response.valid && that._submitIfValid === true) {
                                // If a remote validator returns true and the form is ready to submit, then do it
                                that._submit();
                            } else if (!response.valid && !verbose) {
                                stop = true;
                            }
                        });
                    }
                    // ... or object { valid: true/false, message: 'dynamic message' }
                    else if ('object' === typeof validateResult && validateResult.valid !== undefined && validateResult.message !== undefined) {
                        $field.data('bv.response.' + validatorName, validateResult);
                        this.updateMessage(updateAll ? field : $field, validatorName, validateResult.message);
                        this.updateStatus(updateAll ? field : $field, validateResult.valid ? this.STATUS_VALID : this.STATUS_INVALID, validatorName);
                        if (!validateResult.valid && !verbose) {
                            break;
                        }
                    }
                    // ... or a boolean value
                    else if ('boolean' === typeof validateResult) {
                        $field.data('bv.response.' + validatorName, validateResult);
                        this.updateStatus(updateAll ? field : $field, validateResult ? this.STATUS_VALID : this.STATUS_INVALID, validatorName);
                        if (!validateResult && !verbose) {
                            break;
                        }
                    }
                }
            }

            return this;
        },

        /**
         * Update the error message
         *
         * @param {String|jQuery} field The field name or field element
         * @param {String} validator The validator name
         * @param {String} message The message
         * @returns {BootstrapValidator}
         */
        updateMessage: function(field, validator, message) {
            var $fields = $([]);
            switch (typeof field) {
                case 'object':
                    $fields = field;
                    field   = field.attr('data-bv-field');
                    break;
                case 'string':
                    $fields = this.getFieldElements(field);
                    break;
                default:
                    break;
            }

            $fields.each(function() {
                $(this).data('bv.messages').find('.help-block[data-bv-validator="' + validator + '"][data-bv-for="' + field + '"]').html(message);
            });
        },
        
        /**
         * Update all validating results of field
         *
         * @param {String|jQuery} field The field name or field element
         * @param {String} status The status. Can be 'NOT_VALIDATED', 'VALIDATING', 'INVALID' or 'VALID'
         * @param {String} [validatorName] The validator name. If null, the method updates validity result for all validators
         * @returns {BootstrapValidator}
         */
        updateStatus: function(field, status, validatorName) {
            var fields = $([]);
            switch (typeof field) {
                case 'object':
                    fields = field;
                    field  = field.attr('data-bv-field');
                    break;
                case 'string':
                    fields = this.getFieldElements(field);
                    break;
                default:
                    break;
            }

            if (status === this.STATUS_NOT_VALIDATED) {
                // Reset the flag
                // To prevent the form from doing submit when a deferred validator returns true while typing
                this._submitIfValid = false;
            }

            var that  = this,
                type  = fields.attr('type'),
                group = this.options.fields[field].group || this.options.group,
                total = ('radio' === type || 'checkbox' === type) ? 1 : fields.length;

            for (var i = 0; i < total; i++) {
                var $field       = fields.eq(i);
                if (this._isExcluded($field)) {
                    continue;
                }

                var $parent      = $field.parents(group),
                    $message     = $field.data('bv.messages'),
                    $allErrors   = $message.find('.help-block[data-bv-validator][data-bv-for="' + field + '"]'),
                    $errors      = validatorName ? $allErrors.filter('[data-bv-validator="' + validatorName + '"]') : $allErrors,
                    $icon        = $field.data('bv.icon'),
                    container    = ('function' === typeof (this.options.fields[field].container || this.options.container)) ? (this.options.fields[field].container || this.options.container).call(this, $field, this) : (this.options.fields[field].container || this.options.container),
                    isValidField = null;

                // Update status
                if (validatorName) {
                    $field.data('bv.result.' + validatorName, status);
                } else {
                    for (var v in this.options.fields[field].validators) {
                        $field.data('bv.result.' + v, status);
                    }
                }

                // Show/hide error elements and feedback icons
                $errors.attr('data-bv-result', status);

                // Determine the tab containing the element
                var $tabPane = $field.parents('.tab-pane'),
                    tabId, $tab;
                if ($tabPane && (tabId = $tabPane.attr('id'))) {
                    $tab = $('a[href="#' + tabId + '"][data-toggle="tab"]').parent();
                }

                switch (status) {
                    case this.STATUS_VALIDATING:
                        isValidField = null;
                        this.disableSubmitButtons(true);
                        $parent.removeClass('has-success').removeClass('has-error');
                        if ($icon) {
                            $icon.removeClass(this.options.feedbackIcons.valid).removeClass(this.options.feedbackIcons.invalid).addClass(this.options.feedbackIcons.validating).show();
                        }
                        if ($tab) {
                            $tab.removeClass('bv-tab-success').removeClass('bv-tab-error');
                        }
                        break;

                    case this.STATUS_INVALID:
                        isValidField = false;
                        this.disableSubmitButtons(true);
                        $parent.removeClass('has-success').addClass('has-error');
                        if ($icon) {
                            $icon.removeClass(this.options.feedbackIcons.valid).removeClass(this.options.feedbackIcons.validating).addClass(this.options.feedbackIcons.invalid).show();
                        }
                        if ($tab) {
                            $tab.removeClass('bv-tab-success').addClass('bv-tab-error');
                        }
                        break;

                    case this.STATUS_VALID:
                        // If the field is valid (passes all validators)
                        isValidField = ($allErrors.filter('[data-bv-result="' + this.STATUS_NOT_VALIDATED +'"]').length === 0)
                                     ? ($allErrors.filter('[data-bv-result="' + this.STATUS_VALID +'"]').length === $allErrors.length)  // All validators are completed
                                     : null;                                                                                            // There are some validators that have not done
                        if (isValidField !== null) {
                            this.disableSubmitButtons(this.$submitButton ? !this.isValid() : !isValidField);
                            if ($icon) {
                                $icon
                                    .removeClass(this.options.feedbackIcons.invalid).removeClass(this.options.feedbackIcons.validating).removeClass(this.options.feedbackIcons.valid)
                                    .addClass(isValidField ? this.options.feedbackIcons.valid : this.options.feedbackIcons.invalid)
                                    .show();
                            }
                        }

                        $parent.removeClass('has-error has-success').addClass(this.isValidContainer($parent) ? 'has-success' : 'has-error');
                        if ($tab) {
                            $tab.removeClass('bv-tab-success').removeClass('bv-tab-error').addClass(this.isValidContainer($tabPane) ? 'bv-tab-success' : 'bv-tab-error');
                        }
                        break;

                    case this.STATUS_NOT_VALIDATED:
                    /* falls through */
                    default:
                        isValidField = null;
                        this.disableSubmitButtons(false);
                        $parent.removeClass('has-success').removeClass('has-error');
                        if ($icon) {
                            $icon.removeClass(this.options.feedbackIcons.valid).removeClass(this.options.feedbackIcons.invalid).removeClass(this.options.feedbackIcons.validating).hide();
                        }
                        if ($tab) {
                            $tab.removeClass('bv-tab-success').removeClass('bv-tab-error');
                        }
                        break;
                }

                switch (true) {
                    // Only show the first error message if it is placed inside a tooltip ...
                    case ($icon && 'tooltip' === container):
                        (isValidField === false)
                                ? $icon.css('cursor', 'pointer').tooltip('destroy').tooltip({
                                    container: 'body',
                                    html: true,
                                    placement: 'auto top',
                                    title: $allErrors.filter('[data-bv-result="' + that.STATUS_INVALID + '"]').eq(0).html()
                                })
                                : $icon.css('cursor', '').tooltip('destroy');
                        break;
                    // ... or popover
                    case ($icon && 'popover' === container):
                        (isValidField === false)
                                ? $icon.css('cursor', 'pointer').popover('destroy').popover({
                                    container: 'body',
                                    content: $allErrors.filter('[data-bv-result="' + that.STATUS_INVALID + '"]').eq(0).html(),
                                    html: true,
                                    placement: 'auto top',
                                    trigger: 'hover click'
                                })
                                : $icon.css('cursor', '').popover('destroy');
                        break;
                    default:
                        (status === this.STATUS_INVALID) ? $errors.show() : $errors.hide();
                        break;
                }

                // Trigger an event
                $field.trigger($.Event(this.options.events.fieldStatus), {
                    bv: this,
                    field: field,
                    element: $field,
                    status: status
                });
                this._onFieldValidated($field, validatorName);
            }

            return this;
        },

        /**
         * Check the form validity
         *
         * @returns {Boolean}
         */
        isValid: function() {
            for (var field in this.options.fields) {
                if (!this.isValidField(field)) {
                    return false;
                }
            }

            return true;
        },

        /**
         * Check if the field is valid or not
         *
         * @param {String|jQuery} field The field name or field element
         * @returns {Boolean}
         */
        isValidField: function(field) {
            var fields = $([]);
            switch (typeof field) {
                case 'object':
                    fields = field;
                    field  = field.attr('data-bv-field');
                    break;
                case 'string':
                    fields = this.getFieldElements(field);
                    break;
                default:
                    break;
            }
            if (fields.length === 0 || !this.options.fields[field] || this.options.fields[field].enabled === false) {
                return true;
            }

            var type  = fields.attr('type'),
                total = ('radio' === type || 'checkbox' === type) ? 1 : fields.length,
                $field, validatorName, status;
            for (var i = 0; i < total; i++) {
                $field = fields.eq(i);
                if (this._isExcluded($field)) {
                    continue;
                }

                for (validatorName in this.options.fields[field].validators) {
                    if (this.options.fields[field].validators[validatorName].enabled === false) {
                        continue;
                    }

                    status = $field.data('bv.result.' + validatorName);
                    if (status !== this.STATUS_VALID) {
                        return false;
                    }
                }
            }

            return true;
        },

        /**
         * Check if all fields inside a given container are valid.
         * It's useful when working with a wizard-like such as tab, collapse
         *
         * @param {String|jQuery} container The container selector or element
         * @returns {Boolean}
         */
        isValidContainer: function(container) {
            var that       = this,
                map        = {},
                $container = ('string' === typeof container) ? $(container) : container;
            if ($container.length === 0) {
                return true;
            }

            $container.find('[data-bv-field]').each(function() {
                var $field = $(this),
                    field  = $field.attr('data-bv-field');
                if (!that._isExcluded($field) && !map[field]) {
                    map[field] = $field;
                }
            });

            for (var field in map) {
                var $f = map[field];
                if ($f.data('bv.messages')
                      .find('.help-block[data-bv-validator][data-bv-for="' + field + '"]')
                      .filter('[data-bv-result="' + this.STATUS_INVALID +'"]')
                      .length > 0)
                {
                    return false;
                }
            }

            return true;
        },

        /**
         * Submit the form using default submission.
         * It also does not perform any validations when submitting the form
         */
        defaultSubmit: function() {
            if (this.$submitButton) {
                // Create hidden input to send the submit buttons
                $('<input/>')
                    .attr('type', 'hidden')
                    .attr('data-bv-submit-hidden', '')
                    .attr('name', this.$submitButton.attr('name'))
                    .val(this.$submitButton.val())
                    .appendTo(this.$form);
            }

            // Submit form
            this.$form.off('submit.bv').submit();
        },

        // ---
        // Useful APIs which aren't used internally
        // ---

        /**
         * Get the list of invalid fields
         *
         * @returns {jQuery[]}
         */
        getInvalidFields: function() {
            return this.$invalidFields;
        },

        /**
         * Returns the clicked submit button
         *
         * @returns {jQuery}
         */
        getSubmitButton: function() {
            return this.$submitButton;
        },

        /**
         * Get the error messages
         *
         * @param {String|jQuery} [field] The field name or field element
         * If the field is not defined, the method returns all error messages of all fields
         * @param {String} [validator] The name of validator
         * If the validator is not defined, the method returns error messages of all validators
         * @returns {String[]}
         */
        getMessages: function(field, validator) {
            var that     = this,
                messages = [],
                $fields  = $([]);

            switch (true) {
                case (field && 'object' === typeof field):
                    $fields = field;
                    break;
                case (field && 'string' === typeof field):
                    var f = this.getFieldElements(field);
                    if (f.length > 0) {
                        var type = f.attr('type');
                        $fields = ('radio' === type || 'checkbox' === type) ? f.eq(0) : f;
                    }
                    break;
                default:
                    $fields = this.$invalidFields;
                    break;
            }

            var filter = validator ? '[data-bv-validator="' + validator + '"]' : '';
            $fields.each(function() {
                messages = messages.concat(
                    $(this)
                        .data('bv.messages')
                        .find('.help-block[data-bv-for="' + $(this).attr('data-bv-field') + '"][data-bv-result="' + that.STATUS_INVALID + '"]' + filter)
                        .map(function() {
                            var v = $(this).attr('data-bv-validator'),
                                f = $(this).attr('data-bv-for');
                            return (that.options.fields[f].validators[v].enabled === false) ? '' : $(this).html();
                        })
                        .get()
                );
            });

            return messages;
        },

        /**
         * Update the option of a specific validator
         *
         * @param {String|jQuery} field The field name or field element
         * @param {String} validator The validator name
         * @param {String} option The option name
         * @param {String} value The value to set
         * @returns {BootstrapValidator}
         */
        updateOption: function(field, validator, option, value) {
            if ('object' === typeof field) {
                field = field.attr('data-bv-field');
            }
            if (this.options.fields[field] && this.options.fields[field].validators[validator]) {
                this.options.fields[field].validators[validator][option] = value;
                this.updateStatus(field, this.STATUS_NOT_VALIDATED, validator);
            }

            return this;
        },

        /**
         * Add a new field
         *
         * @param {String|jQuery} field The field name or field element
         * @param {Object} [options] The validator rules
         * @returns {BootstrapValidator}
         */
        addField: function(field, options) {
            var fields = $([]);
            switch (typeof field) {
                case 'object':
                    fields = field;
                    field  = field.attr('data-bv-field') || field.attr('name');
                    break;
                case 'string':
                    delete this._cacheFields[field];
                    fields = this.getFieldElements(field);
                    break;
                default:
                    break;
            }

            fields.attr('data-bv-field', field);

            var type  = fields.attr('type'),
                total = ('radio' === type || 'checkbox' === type) ? 1 : fields.length;

            for (var i = 0; i < total; i++) {
                var $field = fields.eq(i);

                // Try to parse the options from HTML attributes
                var opts = this._parseOptions($field);
                opts = (opts === null) ? options : $.extend(true, options, opts);

                this.options.fields[field] = $.extend(true, this.options.fields[field], opts);

                // Update the cache
                this._cacheFields[field] = this._cacheFields[field] ? this._cacheFields[field].add($field) : $field;

                // Init the element
                this._initField(('checkbox' === type || 'radio' === type) ? field : $field);
            }

            this.disableSubmitButtons(false);
            // Trigger an event
            this.$form.trigger($.Event(this.options.events.fieldAdded), {
                field: field,
                element: fields,
                options: this.options.fields[field]
            });

            return this;
        },

        /**
         * Remove a given field
         *
         * @param {String|jQuery} field The field name or field element
         * @returns {BootstrapValidator}
         */
        removeField: function(field) {
            var fields = $([]);
            switch (typeof field) {
                case 'object':
                    fields = field;
                    field  = field.attr('data-bv-field') || field.attr('name');
                    fields.attr('data-bv-field', field);
                    break;
                case 'string':
                    fields = this.getFieldElements(field);
                    break;
                default:
                    break;
            }

            if (fields.length === 0) {
                return this;
            }

            var type  = fields.attr('type'),
                total = ('radio' === type || 'checkbox' === type) ? 1 : fields.length;

            for (var i = 0; i < total; i++) {
                var $field = fields.eq(i);

                // Remove from the list of invalid fields
                this.$invalidFields = this.$invalidFields.not($field);

                // Update the cache
                this._cacheFields[field] = this._cacheFields[field].not($field);
            }

            if (!this._cacheFields[field] || this._cacheFields[field].length === 0) {
                delete this.options.fields[field];
            }
            if ('checkbox' === type || 'radio' === type) {
                this._initField(field);
            }

            this.disableSubmitButtons(false);
            // Trigger an event
            this.$form.trigger($.Event(this.options.events.fieldRemoved), {
                field: field,
                element: fields
            });

            return this;
        },

        /**
         * Reset given field
         *
         * @param {String|jQuery} field The field name or field element
         * @param {Boolean} [resetValue] If true, the method resets field value to empty or remove checked/selected attribute (for radio/checkbox)
         * @returns {BootstrapValidator}
         */
        resetField: function(field, resetValue) {
            var $fields = $([]);
            switch (typeof field) {
                case 'object':
                    $fields = field;
                    field   = field.attr('data-bv-field');
                    break;
                case 'string':
                    $fields = this.getFieldElements(field);
                    break;
                default:
                    break;
            }

            var total = $fields.length;
            if (this.options.fields[field]) {
                for (var i = 0; i < total; i++) {
                    for (var validator in this.options.fields[field].validators) {
                        $fields.eq(i).removeData('bv.dfs.' + validator);
                    }
                }
            }

            // Mark field as not validated yet
            this.updateStatus(field, this.STATUS_NOT_VALIDATED);

            if (resetValue) {
                var type = $fields.attr('type');
                ('radio' === type || 'checkbox' === type) ? $fields.removeAttr('checked').removeAttr('selected') : $fields.val('');
            }

            return this;
        },

        /**
         * Reset the form
         *
         * @param {Boolean} [resetValue] If true, the method resets field value to empty or remove checked/selected attribute (for radio/checkbox)
         * @returns {BootstrapValidator}
         */
        resetForm: function(resetValue) {
            for (var field in this.options.fields) {
                this.resetField(field, resetValue);
            }

            this.$invalidFields = $([]);
            this.$submitButton  = null;

            // Enable submit buttons
            this.disableSubmitButtons(false);

            return this;
        },

        /**
         * Revalidate given field
         * It's used when you need to revalidate the field which its value is updated by other plugin
         *
         * @param {String|jQuery} field The field name of field element
         * @returns {BootstrapValidator}
         */
        revalidateField: function(field) {
            this.updateStatus(field, this.STATUS_NOT_VALIDATED)
                .validateField(field);

            return this;
        },

        /**
         * Enable/Disable all validators to given field
         *
         * @param {String} field The field name
         * @param {Boolean} enabled Enable/Disable field validators
         * @param {String} [validatorName] The validator name. If null, all validators will be enabled/disabled
         * @returns {BootstrapValidator}
         */
        enableFieldValidators: function(field, enabled, validatorName) {
            var validators = this.options.fields[field].validators;

            // Enable/disable particular validator
            if (validatorName
                && validators
                && validators[validatorName] && validators[validatorName].enabled !== enabled)
            {
                this.options.fields[field].validators[validatorName].enabled = enabled;
                this.updateStatus(field, this.STATUS_NOT_VALIDATED, validatorName);
            }
            // Enable/disable all validators
            else if (!validatorName && this.options.fields[field].enabled !== enabled) {
                this.options.fields[field].enabled = enabled;
                for (var v in validators) {
                    this.enableFieldValidators(field, enabled, v);
                }
            }

            return this;
        },

        /**
         * Some validators have option which its value is dynamic.
         * For example, the zipCode validator has the country option which might be changed dynamically by a select element.
         *
         * @param {jQuery|String} field The field name or element
         * @param {String|Function} option The option which can be determined by:
         * - a string
         * - name of field which defines the value
         * - name of function which returns the value
         * - a function returns the value
         *
         * The callback function has the format of
         *      callback: function(value, validator, $field) {
         *          // value is the value of field
         *          // validator is the BootstrapValidator instance
         *          // $field is the field element
         *      }
         *
         * @returns {String}
         */
        getDynamicOption: function(field, option) {
            var $field = ('string' === typeof field) ? this.getFieldElements(field) : field,
                value  = $field.val();

            // Option can be determined by
            // ... a function
            if ('function' === typeof option) {
                return $.fn.bootstrapValidator.helpers.call(option, [value, this, $field]);
            }
            // ... value of other field
            else if ('string' === typeof option) {
                var $f = this.getFieldElements(option);
                if ($f.length) {
                    return $f.val();
                }
                // ... return value of callback
                else {
                    return $.fn.bootstrapValidator.helpers.call(option, [value, this, $field]) || option;
                }
            }

            return null;
        },

        /**
         * Destroy the plugin
         * It will remove all error messages, feedback icons and turn off the events
         */
        destroy: function() {
            var field, fields, $field, validator, $icon, group;
            for (field in this.options.fields) {
                fields    = this.getFieldElements(field);
                group     = this.options.fields[field].group || this.options.group;
                for (var i = 0; i < fields.length; i++) {
                    $field = fields.eq(i);
                    $field
                        // Remove all error messages
                        .data('bv.messages')
                            .find('.help-block[data-bv-validator][data-bv-for="' + field + '"]').remove().end()
                            .end()
                        .removeData('bv.messages')
                        // Remove feedback classes
                        .parents(group)
                            .removeClass('has-feedback has-error has-success')
                            .end()
                        // Turn off events
                        .off('.bv')
                        .removeAttr('data-bv-field');

                    // Remove feedback icons, tooltip/popover container
                    $icon = $field.data('bv.icon');
                    if ($icon) {
                        var container = ('function' === typeof (this.options.fields[field].container || this.options.container)) ? (this.options.fields[field].container || this.options.container).call(this, $field, this) : (this.options.fields[field].container || this.options.container);
                        switch (container) {
                            case 'tooltip':
                                $icon.tooltip('destroy').remove();
                                break;
                            case 'popover':
                                $icon.popover('destroy').remove();
                                break;
                            default:
                                $icon.remove();
                                break;
                        }
                    }
                    $field.removeData('bv.icon');

                    for (validator in this.options.fields[field].validators) {
                        if ($field.data('bv.dfs.' + validator)) {
                            $field.data('bv.dfs.' + validator).reject();
                        }
                        $field.removeData('bv.result.' + validator)
                              .removeData('bv.response.' + validator)
                              .removeData('bv.dfs.' + validator);

                        // Destroy the validator
                        if ('function' === typeof $.fn.bootstrapValidator.validators[validator].destroy) {
                            $.fn.bootstrapValidator.validators[validator].destroy(this, $field, this.options.fields[field].validators[validator]);
                        }
                    }
                }
            }

            this.disableSubmitButtons(false);   // Enable submit buttons
            this.$hiddenButton.remove();        // Remove the hidden button

            this.$form
                .removeClass(this.options.elementClass)
                .off('.bv')
                .removeData('bootstrapValidator')
                // Remove generated hidden elements
                .find('[data-bv-submit-hidden]').remove().end()
                .find('[type="submit"]').off('click.bv');
        }
    };

    // Plugin definition
    $.fn.bootstrapValidator = function(option) {
        var params = arguments;
        return this.each(function() {
            var $this   = $(this),
                data    = $this.data('bootstrapValidator'),
                options = 'object' === typeof option && option;
            if (!data) {
                data = new BootstrapValidator(this, options);
                $this.data('bootstrapValidator', data);
            }

            // Allow to call plugin method
            if ('string' === typeof option) {
                data[option].apply(data, Array.prototype.slice.call(params, 1));
            }
        });
    };

    // The default options
    // Sorted in alphabetical order
    $.fn.bootstrapValidator.DEFAULT_OPTIONS = {
        // The first invalid field will be focused automatically
        autoFocus: true,

        //The error messages container. It can be:
        // - 'tooltip' if you want to use Bootstrap tooltip to show error messages
        // - 'popover' if you want to use Bootstrap popover to show error messages
        // - a CSS selector indicating the container
        // In the first two cases, since the tooltip/popover should be small enough, the plugin only shows only one error message
        // You also can define the message container for particular field
        container: null,

        // The form CSS class
        elementClass: 'bv-form',

        // Use custom event name to avoid window.onerror being invoked by jQuery
        // See https://github.com/nghuuphuoc/bootstrapvalidator/issues/630
        events: {
            formInit: 'init.form.bv',
            formError: 'error.form.bv',
            formSuccess: 'success.form.bv',
            fieldAdded: 'added.field.bv',
            fieldRemoved: 'removed.field.bv',
            fieldInit: 'init.field.bv',
            fieldError: 'error.field.bv',
            fieldSuccess: 'success.field.bv',
            fieldStatus: 'status.field.bv',
            validatorError: 'error.validator.bv',
            validatorSuccess: 'success.validator.bv'
        },

        // Indicate fields which won't be validated
        // By default, the plugin will not validate the following kind of fields:
        // - disabled
        // - hidden
        // - invisible
        //
        // The setting consists of jQuery filters. Accept 3 formats:
        // - A string. Use a comma to separate filter
        // - An array. Each element is a filter
        // - An array. Each element can be a callback function
        //      function($field, validator) {
        //          $field is jQuery object representing the field element
        //          validator is the BootstrapValidator instance
        //          return true or false;
        //      }
        //
        // The 3 following settings are equivalent:
        //
        // 1) ':disabled, :hidden, :not(:visible)'
        // 2) [':disabled', ':hidden', ':not(:visible)']
        // 3) [':disabled', ':hidden', function($field) {
        //        return !$field.is(':visible');
        //    }]
        excluded: [':disabled', ':hidden', ':not(:visible)'],

        // Shows ok/error/loading icons based on the field validity.
        // This feature requires Bootstrap v3.1.0 or later (http://getbootstrap.com/css/#forms-control-validation).
        // Since Bootstrap doesn't provide any methods to know its version, this option cannot be on/off automatically.
        // In other word, to use this feature you have to upgrade your Bootstrap to v3.1.0 or later.
        //
        // Examples:
        // - Use Glyphicons icons:
        //  feedbackIcons: {
        //      valid: 'glyphicon glyphicon-ok',
        //      invalid: 'glyphicon glyphicon-remove',
        //      validating: 'glyphicon glyphicon-refresh'
        //  }
        // - Use FontAwesome icons:
        //  feedbackIcons: {
        //      valid: 'fa fa-check',
        //      invalid: 'fa fa-times',
        //      validating: 'fa fa-refresh'
        //  }
        feedbackIcons: {
            valid:      null,
            invalid:    null,
            validating: null
        },

        // Map the field name with validator rules
        fields: null,

        // The CSS selector for indicating the element consists the field
        // By default, each field is placed inside the <div class="form-group"></div>
        // You should adjust this option if your form group consists of many fields which not all of them need to be validated
        group: '.form-group',

        // Live validating option
        // Can be one of 3 values:
        // - enabled: The plugin validates fields as soon as they are changed
        // - disabled: Disable the live validating. The error messages are only shown after the form is submitted
        // - submitted: The live validating is enabled after the form is submitted
        live: 'enabled',

        // Default invalid message
        message: 'This value is not valid',

        // The submit buttons selector
        // These buttons will be disabled to prevent the valid form from multiple submissions
        submitButtons: '[type="submit"]',

        // The field will not be live validated if its length is less than this number of characters
        threshold: null,

        // Whether to be verbose when validating a field or not.
        // Possible values:
        // - true:  when a field has multiple validators, all of them will be checked, and respectively - if errors occur in
        //          multiple validators, all of them will be displayed to the user
        // - false: when a field has multiple validators, validation for this field will be terminated upon the first encountered error.
        //          Thus, only the very first error message related to this field will be displayed to the user
        verbose: true
    };

    // Available validators
    $.fn.bootstrapValidator.validators  = {};

    // i18n
    $.fn.bootstrapValidator.i18n        = {};

    $.fn.bootstrapValidator.Constructor = BootstrapValidator;

    // Helper methods, which can be used in validator class
    $.fn.bootstrapValidator.helpers = {
        /**
         * Execute a callback function
         *
         * @param {String|Function} functionName Can be
         * - name of global function
         * - name of namespace function (such as A.B.C)
         * - a function
         * @param {Array} args The callback arguments
         */
        call: function(functionName, args) {
            if ('function' === typeof functionName) {
                return functionName.apply(this, args);
            } else if ('string' === typeof functionName) {
                if ('()' === functionName.substring(functionName.length - 2)) {
                    functionName = functionName.substring(0, functionName.length - 2);
                }
                var ns      = functionName.split('.'),
                    func    = ns.pop(),
                    context = window;
                for (var i = 0; i < ns.length; i++) {
                    context = context[ns[i]];
                }

                return (typeof context[func] === 'undefined') ? null : context[func].apply(this, args);
            }
        },

        /**
         * Format a string
         * It's used to format the error message
         * format('The field must between %s and %s', [10, 20]) = 'The field must between 10 and 20'
         *
         * @param {String} message
         * @param {Array} parameters
         * @returns {String}
         */
        format: function(message, parameters) {
            if (!$.isArray(parameters)) {
                parameters = [parameters];
            }

            for (var i in parameters) {
                message = message.replace('%s', parameters[i]);
            }

            return message;
        },

        /**
         * Validate a date
         *
         * @param {Number} year The full year in 4 digits
         * @param {Number} month The month number
         * @param {Number} day The day number
         * @param {Boolean} [notInFuture] If true, the date must not be in the future
         * @returns {Boolean}
         */
        date: function(year, month, day, notInFuture) {
            if (isNaN(year) || isNaN(month) || isNaN(day)) {
                return false;
            }
            if (day.length > 2 || month.length > 2 || year.length > 4) {
                return false;
            }

            day   = parseInt(day, 10);
            month = parseInt(month, 10);
            year  = parseInt(year, 10);

            if (year < 1000 || year > 9999 || month <= 0 || month > 12) {
                return false;
            }
            var numDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
            // Update the number of days in Feb of leap year
            if (year % 400 === 0 || (year % 100 !== 0 && year % 4 === 0)) {
                numDays[1] = 29;
            }

            // Check the day
            if (day <= 0 || day > numDays[month - 1]) {
                return false;
            }

            if (notInFuture === true) {
                var currentDate  = new Date(),
                    currentYear  = currentDate.getFullYear(),
                    currentMonth = currentDate.getMonth(),
                    currentDay   = currentDate.getDate();
                return (year < currentYear
                        || (year === currentYear && month - 1 < currentMonth)
                        || (year === currentYear && month - 1 === currentMonth && day < currentDay));
            }

            return true;
        },

        /**
         * Implement Luhn validation algorithm
         * Credit to https://gist.github.com/ShirtlessKirk/2134376
         *
         * @see http://en.wikipedia.org/wiki/Luhn
         * @param {String} value
         * @returns {Boolean}
         */
        luhn: function(value) {
            var length  = value.length,
                mul     = 0,
                prodArr = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]],
                sum     = 0;

            while (length--) {
                sum += prodArr[mul][parseInt(value.charAt(length), 10)];
                mul ^= 1;
            }

            return (sum % 10 === 0 && sum > 0);
        },

        /**
         * Implement modulus 11, 10 (ISO 7064) algorithm
         *
         * @param {String} value
         * @returns {Boolean}
         */
        mod11And10: function(value) {
            var check  = 5,
                length = value.length;
            for (var i = 0; i < length; i++) {
                check = (((check || 10) * 2) % 11 + parseInt(value.charAt(i), 10)) % 10;
            }
            return (check === 1);
        },

        /**
         * Implements Mod 37, 36 (ISO 7064) algorithm
         * Usages:
         * mod37And36('A12425GABC1234002M')
         * mod37And36('002006673085', '0123456789')
         *
         * @param {String} value
         * @param {String} [alphabet]
         * @returns {Boolean}
         */
        mod37And36: function(value, alphabet) {
            alphabet = alphabet || '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
            var modulus = alphabet.length,
                length  = value.length,
                check   = Math.floor(modulus / 2);
            for (var i = 0; i < length; i++) {
                check = (((check || modulus) * 2) % (modulus + 1) + alphabet.indexOf(value.charAt(i))) % modulus;
            }
            return (check === 1);
        }
    };
}(window.jQuery));
