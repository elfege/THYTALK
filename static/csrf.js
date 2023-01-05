//source:https://gist.github.com/danielbeardsley/6060418 

const CSRF = (function() {
    window.addEvent('domready', function() {
       /**
        * Setup triggers on the .submit() function and the `submit` event so we
        * can add csrf inputs immediately before the form is submitted.
        */
       $$('form').each(function(form) {
          // Ensure all forms submitted via a traditional 'submit' button have
          // an up-to-date CSRF input
          form.addEvent('submit', function() {
             ensureFormHasCSRFFormField(form);
          });
          // Ensure all forms submitted via form.submit() have an up-to-date CSRF
          // input
          const oldSubmit = form.submit;
          // Wrap the default submit() function with our own
          form.submit = function () {
             ensureFormHasCSRFFormField(form);
             return oldSubmit.apply(form, Array.from(arguments));
          }
       });
    });
 
    /**
     * Generate a new token and store it in the cookie
     */
    function resetToken() {
       /**
        * random() generates a number [0..1] so the first two chars are always
        *'0.' no matter what the base.
        */
        const token = Math.random().toString(36).substring(2,12); // 10 char string
 
       // 30 days is pretty arbitrary, it could be 3 minutes or 3 years.
       Cookie.write('csrf', token, { duration: 30 }); // 30 days
       return token;
    }
 
    /**
     * Ensure the provided Form element has a CSRF token
     * input who's value is up to date.
     */
    function ensureFormHasCSRFFormField(form) {
       csrfInputForForm(form).set('value', CSRF.get());
    }
 
    /**
     * Return the csrf input element for the given form or give it one.
     */
    function csrfInputForForm(form) {
        const csrfInput = form.getElement('.csrf');
       if (!csrfInput) {
          csrfInput = CSRF.formField();
          form.grab(csrfInput);
       }
 
       return csrfInput;
    }
 
    return {
       /**
        * ## CSRF.get()
        *
        * Read the value from the cookie or create and return one
        * if it doesn't exist
        */
       get: function() {
          return Cookie.read('csrf') || resetToken();
       },
 
       /**
        * Returns a new hidden input field with the CSRF token as a value.
        * Used when dynamically creating forms.
        */
       formField: function() {
          return new Element("input", {
             type: 'hidden',
             name: 'csrf',
             'class': 'csrf',
             value: CSRF.get()
          });
       }
    };
 })();