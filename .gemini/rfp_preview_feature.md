# RFP Preview & Confirmation Feature

## Overview
Added a two-step submission process for RFPs that allows users to review technical specifications, pricing details, and product matches before final submission to the RFP list.

## Changes Made

### 1. **New State Variables** (SubmitRFP.jsx)
- `showPreview`: Controls whether to show the preview/review screen
- `confirming`: Tracks the confirmation submission state

### 2. **Modified Submission Flow**

#### Previous Flow:
1. User fills form → Clicks "Submit RFP"
2. System processes (extracts specs, matches products, calculates pricing)
3. Automatically submits to backend
4. Shows results briefly
5. Auto-redirects to RFP detail page

#### New Flow:
1. User fills form → Clicks "Submit RFP"
2. System processes locally (extracts specs, matches products, calculates pricing)
3. **Shows preview screen with all details**
4. **User reviews:**
   - Technical specifications extracted
   - Product matches with match scores
   - Pricing breakdown (material, testing, delivery, urgency)
   - Recommended product highlighted
5. **User decides:**
   - Click "Edit Details" → Returns to form to make changes
   - Click "Send to RFP List" → Confirms and submits to backend
6. Redirects to RFP detail page

### 3. **New Functions**

#### `handleSubmit()`
- Processes RFP locally
- Extracts specifications
- Matches products
- Calculates pricing
- Sets `showPreview = true` instead of submitting

#### `handleConfirmSubmit()`
- New function that handles actual backend submission
- Only called when user clicks "Send to RFP List"
- Submits all processed data to backend
- Redirects to RFP detail page

### 4. **UI Changes**

#### Preview Screen Includes:
1. **Header Section**
   - Clear title: "📋 Review RFP Details"
   - Instructions for user

2. **Specifications Section**
   - All extracted technical specs displayed
   - Type and values shown clearly

3. **Product Matches Section**
   - Top 3 matched products
   - Match scores with color coding
   - Matched specifications highlighted

4. **Pricing Section**
   - Recommended product highlighted
   - Complete breakdown:
     - Unit price
     - Quantity
     - Material cost
     - Testing cost
     - Delivery cost
     - Urgency adjustment (if applicable)
   - Alternative options shown

5. **Action Buttons**
   - "← Edit Details" - Returns to form
   - "✓ Send to RFP List" - Confirms submission (olive green, prominent)

#### Conditional Rendering:
- Form and info box hidden when `showPreview = true`
- Preview shown only when `showPreview = true`
- Processing indicator shown during initial processing

## Benefits

1. **User Control**: Users can review all details before committing
2. **Error Prevention**: Catch issues before submission
3. **Transparency**: See exactly what the system extracted and calculated
4. **Flexibility**: Easy to go back and edit if needed
5. **Confidence**: Users know exactly what they're submitting

## Testing Instructions

1. Navigate to "Submit New RFP" page
2. Fill in RFP details (or use "Fill Sample Data")
3. Click "Submit RFP"
4. Wait for processing to complete
5. Review the preview screen showing:
   - Technical specifications
   - Product matches
   - Pricing details
6. Test "Edit Details" button - should return to form
7. Fill form again and process
8. Click "Send to RFP List" - should submit and redirect
9. Verify RFP appears in the list with all details intact

## Files Modified
- `frontend/src/pages/SubmitRFP.jsx`
