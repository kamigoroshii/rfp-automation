/**
 * Quick diagnostic check for SubmitRFP page
 * Run this in browser console on the Submit RFP page
 */

console.log('=== Submit RFP Diagnostic ===');

// Check if form exists
const form = document.querySelector('form');
console.log('Form found:', !!form);

// Check if submit button exists  
const submitBtn = document.querySelector('button[type="submit"]');
console.log('Submit button found:', !!submitBtn);
if (submitBtn) {
    console.log('Submit button text:', submitBtn.textContent);
    console.log('Submit button visible:', submitBtn.offsetParent !== null);
}

// Check all buttons
const allButtons = document.querySelectorAll('button');
console.log('Total buttons on page:', allButtons.length);

// Check form structure
if (form) {
    console.log('Form children count:', form.children.length);
    const submitBtns = form.querySelectorAll('button[type="submit"]');
    console.log('Submit buttons in form:', submitBtns.length);
}

console.log('=== End Diagnostic ===');
