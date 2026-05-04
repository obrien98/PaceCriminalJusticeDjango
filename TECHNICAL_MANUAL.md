# Pace Criminal Justice Society Website Technical Manual

## Purpose Of This Manual

This document explains how the Criminal Justice Society website works in plain language.

It is written for club leaders and future student officers who may need to:

- update leadership information
- add or edit events
- manage gallery photos
- review contact form submissions
- understand which parts of the site are safe to edit

The goal is not to teach Django programming. The goal is to help you manage the website confidently without breaking it.

## What This Website Is

This is a Django website.

In simple terms, that means:

- the website content is partly stored in a database
- the admin panel lets you update important content without editing code
- the site templates and styling files control how things look

Most routine edits should be made in the Django admin panel, not by changing code files.

## The Safest Way To Make Changes

For non-technical users, use the Django admin panel for:

- officers / leadership
- events
- gallery images
- contact form submissions

You should only edit code files if:

- you want to change wording that is hardcoded in the page design
- you want to change colors, layout, or structure
- you want to add new features

## How To Access The Admin Panel

Go to:

`/admin/`

Example:

`https://your-site-url/admin/`

After logging in, you will see the main editable content areas:

- `Officers`
- `Events`
- `Gallery images`
- `Contact messages`

## What To Edit In Admin

### Officers

Use `Officers` to manage the leadership section.

Fields:

- `name`: officer’s name
- `role`: position title
- `email`: optional contact email
- `bio`: short leadership bio
- `image`: headshot or officer photo
- `display_order`: controls the order shown on the website

Tips:

- lower `display_order` numbers appear first
- if no image is uploaded, the site uses a default fallback image

### Events

Use `Events` to manage the event listings.

Fields:

- `name`: event title
- `date`: event date
- `time`: event time
- `location`: where the event is happening
- `description`: extra details for the event detail page

How events appear:

- the homepage shows only a small number of events so the page does not get crowded
- the full events page shows all events
- each event can be clicked for its own detail page

### Gallery Images

Use `Gallery images` to manage photo content.

Fields:

- `title`: internal title for the image
- `image`: the uploaded photo
- `alt_text`: short description for accessibility
- `is_featured`: decides if the image should appear on the homepage
- `display_order`: controls image order

How gallery images appear:

- the homepage shows featured images, or a limited set if nothing is marked featured
- the full gallery page shows all uploaded images

Recommended workflow:

1. Upload many gallery images over time.
2. Mark a smaller set as `is_featured`.
3. Use `display_order` to control which featured images appear first.

### Contact Messages

Use `Contact messages` to review messages submitted through the contact form.

Fields include:

- first name
- last name
- email
- subject
- message
- submitted date
- resolved status

How it works:

- every form submission is saved in the database
- the site also attempts to email the club using the configured email service
- if email sending fails, the message is still saved in admin

## What Files Matter Most

This section explains the most important files in the project.

### Project Entry Files

#### `manage.py`

Used for Django commands such as:

- running the server
- migrations
- tests
- admin-related maintenance

Most non-technical users do not need to edit this.

### Main Project Settings

#### `main_project/settings/base.py`

Shared settings used by the whole project.

This includes:

- installed apps
- static file setup
- media storage
- email settings

Only edit this if you understand Django settings or are following a developer guide.

#### `main_project/settings/dev.py`

Local development settings.

Used when working on the site on a personal machine.

#### `main_project/settings/prod.py`

Production settings.

Used for the live deployed website.

This is where live site behavior is controlled for:

- security
- production hosting
- media serving

### URL Routing

#### `main_project/urls.py`

The main router for the whole website.

It connects the project to the `core` app and controls media serving rules.

#### `core/urls.py`

The page routes for the main club site.

Examples:

- homepage
- gallery page
- events page
- event detail pages

### Models

#### `core/models.py`

This defines the main database content types:

- `Officer`
- `Event`
- `ContactMessage`
- `GalleryImage`

If you add or change database fields, this file changes.

Important note:

Changing `models.py` usually requires running a migration. That is a technical task and should be done carefully.

### Admin Configuration

#### `core/admin.py`

This controls how content appears in the Django admin panel.

If the admin list view changes, or new fields are searchable/filterable, this file is often involved.

### Forms

#### `core/forms.py`

This controls the contact form fields and placeholders.

If you want to change:

- field labels
- placeholder text
- which fields appear

this is one of the main files involved.

### Views

#### `core/views.py`

This is the logic behind the pages.

It decides:

- what content appears on each page
- which events show on the homepage
- which gallery images show on the homepage
- what happens when someone submits the contact form

If a page behaves incorrectly, this file is often part of the cause.

### Templates

Templates control what the HTML page looks like.

#### `templates/base.html`

This is the shared site wrapper.

It contains:

- navbar
- footer
- top-level success/warning messages

If something should appear on every page, it may belong here.

#### `core/templates/core/index.html`

This is the homepage.

It contains sections like:

- hero area
- about section
- leadership section
- gallery section
- events section
- contact form

Many homepage text edits can be made here.

#### `core/templates/core/gallery_list.html`

This is the full gallery page.

#### `core/templates/core/event_list.html`

This is the full events page.

#### `core/templates/core/event_detail.html`

This is the page for a single event.

### Styling

#### `core/static/core/styles/base.css`

Global shared styles.

#### `core/static/core/styles/navbar.css`

Navbar and mobile menu styling.

#### `core/static/core/styles/index.css`

Most homepage styling and shared card/grid styling.

#### `core/static/core/styles/lightbox.css`

Styles for the image lightbox popup.

### JavaScript

#### `core/static/core/scripts/scroll_animations.js`

Controls reveal-on-scroll animations.

#### `core/static/core/scripts/lightbox.js`

Controls the popup/lightbox when users click gallery images.

## What Non-Technical Users Can Edit Safely

These edits are safe in admin:

- add, remove, or reorder officers
- add, remove, or edit events
- upload gallery images
- choose which gallery images are featured
- read contact form submissions
- mark contact messages as resolved

These edits are usually safe in templates if you are careful:

- changing visible paragraph text
- changing headings
- changing button wording

These edits are not recommended unless a developer is helping:

- changing Python files
- changing settings files
- changing database model fields
- changing deployment configuration

## Common Tasks

### Add A New Officer

1. Log into `/admin/`
2. Open `Officers`
3. Click `Add`
4. Fill in the officer information
5. Upload an image if available
6. Set `display_order`
7. Save

### Add A New Event

1. Log into `/admin/`
2. Open `Events`
3. Click `Add`
4. Fill in the event information
5. Save

### Add Gallery Photos

1. Log into `/admin/`
2. Open `Gallery images`
3. Click `Add`
4. Upload an image
5. Add `title`
6. Add `alt_text`
7. Set `display_order`
8. Turn on `is_featured` if you want it on the homepage
9. Save

### Review Contact Messages

1. Log into `/admin/`
2. Open `Contact messages`
3. Read the message details
4. Mark `is_resolved` when handled

## If Something Looks Wrong

### Gallery Images Are Missing

Check:

- the image uploaded successfully
- Cloudinary is configured correctly
- the image record exists in admin

### Contact Form Saved But No Email Arrived

Check:

- the message exists in `Contact messages`
- SendGrid settings are correct
- the sender email is verified

Important:

The site is designed so contact messages still save in the database even if email sending fails.

### Homepage Looks Too Crowded

Check:

- too many featured gallery images
- too many featured events

The homepage is intentionally designed to show only a smaller curated set.

## Recommended Editing Rules For The Club

To keep the site consistent:

- use the admin panel for almost all content edits
- keep officer bios short
- use consistent event titles
- mark only the best few gallery images as featured
- do not edit Python or settings files unless a developer is assisting

## Developer Notes

If a future student developer inherits this project, the most important things to know are:

- homepage content is intentionally curated for events and gallery
- contact form submissions save to the database and also attempt email delivery
- media uploads may use Cloudinary depending on environment variables
- production and development settings are split into separate files

## Final Advice

If you are unsure whether a change belongs in admin or in code, the answer is usually:

- content change: use admin
- design/behavior change: use code

When in doubt, make a small change first, save, and preview it before doing a large batch of edits.
