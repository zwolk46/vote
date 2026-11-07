# TASTE — Zach's design taste, carried from the midterms site

This file carries the design taste of Zach (the maker) from the election-results site (zwolk46/midterms) to a new site, a visualization of the statistical importance of one vote. Every quotation below is copied verbatim from `RULINGS.md` in zwolk46/midterms (2026-11-02 to 2026-11-06); cut only with an ellipsis, never reworded. Each is evidence of his taste. Unless he rules otherwise in the new project, it stands there as the default, so an agent applies it without asking him again. The sentence after each quote says what it means for any site. Where an entry has no quotation marks, the record gave only the orchestrator's summary of his remark, and it is marked "(record's summary)". Dates and times are UTC as given.

A remark about elections only was left out (see "Left out" at the end).


> **Superseded in part (2026-11-07 02:45 UTC).** The rulings under "Components and where they come from" that require every part to be a found, real component, and that forbid designing in-house, no longer bind. The maker: "I think I was too strict about using real components, and it would have been better probably to leave a little bit of the design and the creativity to you or whatever agent was working". Components he names himself are still built from. See `README.md`, process step 1.

## Faults he named (what reads as AI-made or careless)

- **2026-10-23.** Soft drop shadows separating cards, called "peak AI default design". Do not separate cards with soft shadows.
- **2026-10-24.** (record's summary) The tells of a generic AI-made site he listed: hover glows and shadows, moving arrows, dots that pulse for nothing live, text scrolling across the screen, numbers on things not in sequence, filler text. Each is a fault.
- **2026-11-02 13:17:57 UTC.** "unless the subheaders, like the extra text below the title of what the thing is showing, is actually needed, like if I actually have to read it in order to understand what's going on, then include it. Otherwise, it is a characteristic of AI-generated websites, and like the subheading, the extra text is simply not needed and it wastes space." Under a title, and anywhere, include text only if the viewer must read it to understand what is shown.
- **2026-11-02 13:17:57 UTC.** "Why the hell would a website need to say what font is used inside the website?" Never describe the site's own build (fonts, tools) on the site.
- **2026-11-02 13:21:33 UTC.** "It doesn't need to say governors twice." (the record has: "it says governors, 39 races, and then under that, governors. It doesn't need to say governors twice.") Never repeat a heading or label.
- **2026-11-02 21:20 UTC.** "Those are like, they use the standard symbols that AI-generated content uses, and I do not want that. I want good icons, like maybe Hero UI icons, which I have access to, or something else. But like, avoid all that AI stuff." No stock keyboard-hint glyphs or default icon symbols; every icon comes from one chosen, real icon set.
- **2026-11-03 16:16 UTC.** "the arrow is one of the triangle standard default AI icons. I want that deliberately removed." A default play-triangle or arrow is removed, not swapped.
- **2026-11-03 16:16 UTC.** "The change being very similar to the kind of change to make when removing excess text. They're made for the same reason." Stock icons are removed for the same reason as excess text: if the words or layout already carry the meaning, the mark goes.
- **2026-11-05 20:45 UTC.** "the two letters should be centered and the arrow should be a real arrow, not one of the standard glyphs." Use a drawn arrow, not a text glyph, and centre the letters beside it.
- **2026-11-05 14:21 UTC.** "A big part of this will be removing unnecessary text and distilling visual representations. Visual keys are better than long paragraphs at the bottom of the page, etc." Replace explanatory paragraphs with visual keys (legends, swatches); a key beats a paragraph at the foot of the page.
- **2026-11-04 19:10 UTC.** "please remove the extra text below the tab selector, closest first by state and by topic." Remove explanatory lines under tab or segmented controls.
- **2026-11-03 11:50 UTC.** "There's no like New York homepage or state homepage or district page at all. So if I were to click on the like the Attorney General for New York's race and click the back button, which says New York, it would do nothing at all." A control that names a place must go there; no dead links or buttons.
- **2026-11-02 13:21:33 UTC.** "There's also in the dropdown, there's an option to select state. And selecting state does nothing." A placeholder option that does nothing is a fault.
- **2026-11-02 13:08:35 UTC.** "The state outlines on hover, sometimes a thick outline sometimes a thin outline and sometimes combined for a single state; shouldn't be that way." A hover or focus outline must be one consistent outline.

## What he loves (the bar to match)

- **2026-10-24.** (record's summary) The navigation menus of details.so were the first components he loved: precise, fluid, natural, integrated with the page.
- **2026-11-02 14:40:36 UTC.** "Some of the changes you've made are EXCELLENT, like great job implementing broadly what I wanted. Now, I want you to understand the reasoning behind the changes I wanted made, and I want similar kinds of changes made elsewhere in the app, as relevant." Read his corrections as principles and apply them everywhere they fit, unprompted.
- **2026-11-05 13:39 UTC.** "it started and remains as one of the most detailed and perfectly crafted components; it's just that things have been added to it." A well-crafted component is protected; additions must not clutter it.
- **2026-11-05 13:50 UTC.** "one of my favorite changes that was implemented, which was a creative change, was the bar to semicircle change. That was excellent, as is the navigation menu on the side." Creative, data-faithful transformations between views are welcome and prized.
- **2026-11-05 16:15 UTC.** "The charts and graphs with transitions are EXCELLENT EXCELLENT EXCEPLENT YESSSS like one thing that made me jealous of the New York Times was that they had a lot more COOL data about the elections that offered so many insights and the transitions like with dots were super super nice." Charts whose marks (dots) move smoothly between states are the favourite kind of display.
- **2026-11-05 18:57 UTC.** "You did a terrific job with like moving the dots around. For example, closest on-call races, terrific." Elements that glide from where they were to where they go are the reference for every transition.
- **2026-11-05 14:15 UTC.** "Making their faces appear on the site would make it SO SO SO much better like SO much better." People's faces make a site feel real; use them where people are named.
- **2026-11-05 15:39 UTC.** "I also want the faces to be a substantial part of the site. They make it feel wayyy more interactive and real!" Images of real people are central, not decoration.
- **2026-11-04 21:28 UTC.** "It should just be smooth from end to end." A transition has no pop or snap at its ends.

## Components and where they come from

- **2026-11-02 13:08:35 UTC.** "I don't feel like I'm seeing lots of components taken directly from sites with nice prebuilt components. Sure, not all fit here, but certainly some do." Use well-made prebuilt components where they fit.
- **2026-11-02 14:41:27 UTC.** "some of the things I want are TRUE menus and cards, and TRUE transitions, like human-made and human-perfected" Menus, cards and transitions should be real, human-crafted components, not agent approximations.
- **2026-11-02 15:39 UTC.** "keep in mind that I'd like to download or have all of the components so I need not keep the subscription other than to access NEW components in the future." Keep components in the repo; do not depend on a subscription to see them.
- **2026-11-02 18:52 UTC.** "I wanna see relevant components found from the web! And from details.so!" Bring real components found on the web and from his components library, shown in a preview he can see.
- **2026-11-02 20:40 UTC.** "for components such as the switch between governor/senate tabs, I want those pulled from REAL components with REAL motion." Every switch, tab row or toggle is a real component with its own motion.
- **2026-11-02 20:45:43 UTC.** "keep in mind the comment I made about the tab . It's not just about that specific tab . There's some reasoning behind it" A remark about one control is a principle for all controls.
- **2026-11-02 20:45 UTC.** "For the things from details.so, I want them actually implemented. Inside the preview, because I can't see them. Like, if they're just linked, I can't see them because I'm not signed in." Show candidate components running inside the preview, not as links he cannot open.
- **2026-11-02 21:20 UTC.** "maybe use the Mobin MCP or details.so to get inspiration for various components. So like, it could be the search, it could be even the bottom part of the search, it could be sections within the search, it could be drawers, menus, literally anything. Like, everything should have real inspiration." Every component, down to its sections and foot, is designed from a named real example.
- **2026-11-02 21:39 UTC.** "You MUST look at the implementations. So far only one seems perfect and EVERYTHING else looks off somehow. Either it is a white topbar on a white background so literally nothing is visible, or the popout is squished in the corner and thus has very weird behavior" Look at each ported component running, at real frame sizes, against its source; that it loads is not a check.
- **2026-11-02 21:42 UTC.** "another reason I want the website is simply to, like, demonstrate my use of the really cool components." Finding true uses for good components is itself a goal of the site.
- **2026-11-03 13:00 UTC.** "If a drawer is needed anywhere on the site I want the Cupertino pane to be used. Also, where the drawer need not be opened in full screen to show more relevant information, open it halfway. It may be that the site doesn't use drawers anyway." Drawers use the Cupertino Pane library and open halfway unless the content needs full screen; do not add a drawer unless needed.
- **2026-11-05 17:35 UTC.** "Like, if there's like an invite card, like a very special component to be found online, I would love that." For a special element, search for a special found component rather than a plain one.
- **2026-11-05 17:45–17:50 UTC.** "I want this component implemented as the logo's hero or something:" A 21st.dev component he found was placed as the entrance hero; he will hand over a specific component and expect a faithful port.
- **2026-11-05 18:26 UTC.** "you might be able to find other components on 21st.dev or details.so or mobin, things like that." The three sources to search first are 21st.dev, Details and Mobbin.
- **2026-11-05 21:03 UTC.** "making your own components is hardly ever the best thing to do. So I don't even want you to come up with the ideas yourself. I don't think the orchestrator should. I think another agent should, after receiving like guidance on what the principles behind why we would include something or something like that, and then it should go through the sites, MCPs, and connectors I have access to and pull actual components." For design-specific parts, a separate sourcing agent, given principles and reasons only, pulls real components; the orchestrator does not invent them.
- **2026-11-05 21:03 UTC.** "Mobin has screens, so you can take ideas from like the flow or the screen or something like that and how maybe a scroll works." Mobbin supplies flows, screens and scroll behaviour as references.
- **2026-11-05 22:29 UTC.** "It doesn't HAVE to be STRICTLY premade components, because that might also cause issues." Purity of origin is not the aim; the best result running is. Judge each ported component by how it runs.
- **2026-11-05 22:29 UTC.** "because they were dots I think it's easy enough for you to control them well through code." Simple data-driven marks (dots) can be written in code; sourced components are for the complex parts.
- **2026-11-05 12:37 UTC.** "Base it on Mobbin examples and Details.so examples, as relevant." Base new displays on real examples from Mobbin and Details.
- **2026-11-05 12:39 UTC.** "I want the system to think about how other apps and sites display data like that, like stocks or something maybe." Study how established products display similar data (for example, price charts in stock apps).
- **2026-11-05 21:04 UTC.** "it's always nice to be able to have like an SVG of their logos presented wherever it's relevant." Where a named company or source appears, show its real logo as inline SVG.
- **2026-11-05 14:21 UTC.** "I'd also like a footer implemented, ideally one that's like details.so. A really cool footer or a normal one, up to you" A footer chosen from real examples, either distinctive or plain.

## Motion

- **2026-11-02 11:36:55 UTC.** "Only fix is spending more deliberate time on motion. Thoroughly research motion for agents, as I am very concerned that a single kind of motion applied everywhere will not work. Motion should satisfy its surface's purpose, not be there just because." Choose motion per surface for its purpose; never one motion everywhere, and none where it serves nothing.
- **2026-11-02 13:08:35 UTC.** "For counts arriving, I want the faded highlight, because it is vital that I am aware what is current, what is recently updated, how old, etc." Changed live figures get a fading highlight so freshness is visible.
- **2026-11-02 13:21:33 UTC.** "So it would also be cool to have transitions between pages." Page transitions are wanted.
- **2026-11-02 20:45 UTC.** "I would rather something like I guess the silk sheet is good enough." He prefers the feel of a real sheet that rises from the bottom.
- **2026-11-03 15:23 UTC.** "when clicking on house from the country homepage, the bar squishes and extends then pops into place like it snaps very nastily. Try checking the motion with screenshots if that's helpful" A bar must not squish, stretch and snap across a view change; remove the animation or fix it fully, and check motion with frame screenshots.
- **2026-11-03 15:39 UTC.** "the card functionality needs a big overhaul and a check of the motion itself, so screenshots will be needed for how swipe interactions work." Check swipe and drag motion with frame captures.
- **2026-11-04 20:06 UTC.** "there's no transition between the semicircle and the bar, and they carry the same information. So I was thinking about if the semicircle transitions from curved to flat, like on curves up, while like the colors blend really nicely." Two views of the same data should morph into each other, not swap.
- **2026-11-04 21:28 UTC.** "the most important thing is at the ends of the animations, there's still a little bit of popping and snapping where there shouldn't be. It should just be smooth from end to end." Check the first and last frames of every animation for pop or snap.
- **2026-11-05 14:18 UTC.** "For the market data I want nice transitions when the tabs are switched, like the lines should move smoothly or something" On switching a chart's tab, the lines move smoothly to the new values.
- **2026-11-05 18:57 UTC.** "clicking replay the night has basically zero visual transition. Clicking now, like everything jumps. And as you know, I hate jumping and I like smooth transitions." Switching between two states of the page must animate every value and mark from where it is to where it goes.
- **2026-11-05 19:00 UTC.** "give the search feature a little bit of a transition, because it's just an instant on off the search overlay." An overlay opens and closes with a motion, not instantly.
- **2026-11-05 16:13 UTC.** "I would also like deliberate motion on touches, and a very, very, like the most deliberate transition, most deliberate page transition of the entire site between hitting the enter button and seeing the home screen." Press and touch feedback is designed, and the entrance has the most deliberate transition on the site.
- **2026-11-05 16:23 UTC.** "I want like some latent thing that always happens. Like there should always be motion on that page, on the sign-in page." The entrance page carries ambient motion that never stops.
- **2026-11-05 16:13 UTC.** "maybe the dots, like the semicircle, they flash or something like that. Something very in line with the style of the site." Background motion should be in the site's own visual language (its dots), not a generic effect.
- **2026-11-05 18:25 UTC.** "There's a little bit of snapping at the end of the animation. Also, I don't think that the other things in the background should appear until the glass animation is done. I also think it should be larger, and each element should deliberately appear." Sequence an entrance: the hero alone first, then each element appears on purpose, in turn; no snap at the end.
- **2026-11-05 18:25 UTC.** "more noticeable motion, maybe like red and blue flickers for the dots, or like a waving flag animation. I want as much effort to be put into that as possible." The entrance should be big, loud and exciting; effort is wanted there above all.
- **2026-11-05 20:58 UTC.** "The sign-in page should make use of like scrolling animations" Use scroll-driven animation on the entrance page.
- **2026-11-05 20:58 UTC.** "as one scrolls down, the dots could scatter out in, out and up and to the side in different directions, maybe. And the logo could pulsate for, or shimmer, or, like, whatever you think the style of the site is." Scroll can drive the dots scattering; the logo may shimmer in a way that fits the site.

## Type and text

- **2026-11-02 13:08:35 UTC.** "There's also a LOT of text, and a lot of it looks the same. I'd like more deliberate separation of elements (doesn't mean MORE, but deliberate, and some could have different formatting, as truly relevant). Get at the heart of what I don't want here." Text that all looks alike is the fault; separate by deliberate formatting, not by adding elements.
- **2026-11-04 19:10 UTC.** "the section titles are the same size and font as all the text below them, so I can't even see the next section." Section headings must be clearly larger and different from body text.
- **2026-11-05 19:30 UTC.** "The visual hierarchy in the search pop-up is not great. The section headers are way smaller and a less noticeable font than the page titles, which is not acceptable." Section headers in any overlay follow the same hierarchy as page titles.
- **2026-11-04 19:21 UTC.** "within a single section, the information there is still a little bit hard to read. Like, what do I want to see first, right? I can find the information I need, which is good, but there's a lot on the page, and there should be very, very deliberate visual hierarchy." In each block, one thing is first by size, weight and room, and the rest steps down.
- **2026-11-04 21:58 UTC.** "Include 2026 to the right of the word Midterms for the logo. The style of the words midterms and 2026 should be distinct. Be deliberate. Wherever the logo apppears it should be the flag icon, then Midterms 2026 or Midterms2026" A logo's parts differ in style (here by weight and value) and appear identically everywhere.
- **2026-11-02 23:54 UTC.** "the only thing I want you to change for the logo is the 2026 is too far away from the word midterms. So I want that to be closer." Related words in a lockup sit close; check spacing between parts.
- **2026-11-04 18:23 UTC.** "I want things as normalized as possible, as for instance I've seen yes/no votes both labeled nonpartisan and that is definitely leftover from it being used for candidates that have no other classification." A label left over from another use of a component must not appear where it is wrong; normalize labels per kind of item.
- **2026-11-05 13:34 UTC.** "Fix the breadcrumbs and make sure all of the pages that exist still follow the standard" One standard for navigation text, applied to every page.
- **2026-11-03 20:52 UTC.** "where there's now one breadcrumb, almost a breadcrumb, it's basically a back button. I want actual breadcrumbs." Use real breadcrumbs (Home, then each level, each a link but the last), not a back button dressed as one.
- **2026-11-03 15:44 UTC.** "I want the text above the state name (such as where it says "New York • Statewide Race" removed, as the info is redundant." Drop a kicker line above a name when it repeats what is shown below.

## Colour and dark mode

- **2026-11-03 14:23 UTC.** "The colors though should be like dark navy red and white" Palette direction for the brand: dark navy, red and white.
- **2026-11-02 20:40 UTC.** "I want light/dark mode options." Offer light, dark and system, remembered on the device.
- **2026-11-03 13:13 UTC.** "The menu itself should respond to the light dark changes. Currently it always stays dark." Every surface follows the chosen scheme, the menu included.
- **2026-11-03 20:53 UTC.** "in dark mode, the pin icon is black, so it can barely be seen. There might be some other issues in dark mode that I'd want checked" Check every icon and surface in dark mode on your own; an icon that vanishes in a scheme is a defect.
- **2026-11-04 21:59 UTC.** "the white lines of the flag symbol must always be white not transparent" White marks in an illustration are solid white in every scheme.
- **2026-11-05 20:58 UTC.** "I want it to be red and white and blue, because otherwise it looks something like Republican, and well, it's just a data displayer, it's not right or left." Do not let a single party-like colour dominate a neutral display; use a balanced palette. (For the new site: avoid a colour that carries a political meaning unless the data does.)
- **2026-11-05 18:35 UTC.** "The background of the admit one cards should probably be red, but I want you to keep that style because the style is cool." Change a colour without losing the style of the component.

## Layout and separation

- **2026-11-02 13:21:33 UTC.** "the vertical line going through it is not the easiest to see. And also the blue red lines are a little bit basic, so maybe they could be pill shaped or be special in some way." Plain rectangles read as basic; markers must be easy to see, and bars may be pill-shaped.
- **2026-11-02 14:54:59 UTC.** "I don't really like full pages that are totally blank." A view must not be almost entirely empty; open in place, as a pop-up, or as a fuller page.
- **2026-11-02 14:54:59 UTC.** "I would like to be able to maybe favorite races or pin them or move cards around as I see fit. I think sometimes cards can work really well. But consider that in light of what they might be used for." Let viewers pin and reorder; use cards only where they fit.
- **2026-11-04 15:06 UTC.** "What I really, really like is the organization of the top part. So Senate, House, and Governors, the numbers, the colors, etc." A tight block of big numbers and colours is the model for other sections.
- **2026-11-04 15:06 UTC.** "they were simply thrown below a dashed line, which kind of makes the organization messy. It does the same thing as lots of text bunched together." Content thrown under a divider is the same fault as bunched text; every block needs its own designed space.
- **2026-11-04 15:06 UTC.** "I want you to be very, very deliberate about the visuals, the visual separation that's required to show this thing on the homepage." Design the visual separation for each new block deliberately.
- **2026-11-04 15:12 UTC.** "I do not want drop downs with way too many options." A chooser lists only the few options that matter, plus an "all".
- **2026-11-04 18:43 UTC.** "to have the option to select different views... and to show like exactly the same functional information, but in a different kind of view." Offer alternative views of the same data behind a switch, with the same figures.
- **2026-11-04 19:10 UTC.** "I would also like the ability to like select which section I want to look at" A long page offers a row of its sections to jump to.
- **2026-11-04 19:21 UTC.** "I want them maybe centered on the page because they look a little bit weird being left justified." Centre a self-contained graphic on the page.
- **2026-11-04 19:24 UTC.** "I want you to be very deliberate about applying the same visual hierarchy principles, very deliberate visual hierarchy principles, and you can do some searching, some research online if you think that would help. And I want you to apply that to any other part of the site that you think is visually crowded with data." A principle fixed once is applied across every crowded page, with research.
- **2026-11-04 18:40 UTC.** "the name AL-1, AZ-1, AR-1, etc. overlap with the line that shows when a race is called." Labels must not overlap marks or rules.
- **2026-11-04 18:40 UTC.** "upon scrolling on the right side, it appears that the state doesn't change, but the state should change... It should be where the scroll is." A companion panel follows the scroll position, not the cursor, with a fade between states.
- **2026-11-04 02:07 UTC.** "I want that information to be as absolutely well organized as possible. Like, think about what information I want to see... I like that you have the coloring because that makes Republican or Democrat perfectly obvious." For a list of events, decide which facts matter and lay them out compactly; party colour makes a side obvious at a glance.
- **2026-11-04 02:07 UTC.** "At least on desktop, the section of the night's calls and what's left to call gets really long when I click all calls and closings. And it's also just on the right side, so it looks extraordinarily awkward." Long lists must not stretch a lopsided column; reorganize them.
- **2026-11-05 15:35 UTC.** "A lot of text is starting to get squished together on mobile. As more information is added, more visual distinctions are necessary." As content grows, add visual distinction; do not let it crowd.
- **2026-11-05 15:38 UTC.** "be very deliberate with the KINDS of information, what information should be seen for what purpose, what info should live near other information, how information should be findable, which information hidden and selectable, etc" Design the information architecture before spacing: what is seen at once, what is folded, what groups with what.
- **2026-11-05 19:04 UTC.** "the home page... have gotten a little bit cluttered. So maybe, I don't know, somewhere there could be like a table of sections or something like that, but really nicely and beautifully implemented with nice motion" A cluttered page gets a beautifully made table of sections.
- **2026-11-05 19:06 UTC.** "I want deliberate consideration of what information is important and needs to come first." Order by importance, with reasons.
- **2026-11-05 19:06 UTC.** "what's shown for a called race is not as beautiful as it could be." A resolved or finished state of a card gets its own deliberate design.
- **2026-11-05 18:09 UTC.** "I want the declared winner card to look better! Be deliberate with it." Every part of a special-state card is chosen and named, not inherited from a list row.
- **2026-11-05 20:35 UTC.** "a standard that we establish that applies for some candidates should apply for all." One standard applies to every item of a kind, not only the ones first noticed.
- **2026-11-05 20:49 UTC.** "the line that's drawn on the left side, the blue line for Kay Conley, is too close to the left side of the circle that surrounds her fake image. And then also her image is not centered with Walter's image." Keep clearance between an edge rule and a portrait; align portraits with each other.
- **2026-11-05 20:49 UTC.** "like whatever you did on the country homepage, I want you to do for those pages, but considering all the kinds of pages that exist and the kinds of info that need to be displayed." Carry a layout fix to every kind of page, adapted to its content.
- **2026-11-05 20:39 UTC.** "The aggregate traded figure should show the sum of polymarket and call sheet, not just polymarket, because that's kind of ridiculous." An aggregate must aggregate all its parts, with the split beneath.
- **2026-11-05 20:45–20:51 UTC.** "no numbers needed because the numbers used elsewhere, and so duplicates of things are unnecessary." Do not repeat a figure shown elsewhere on the page.
- **2026-11-03 18:09 UTC.** "The positioning of names is really off, particularly when there is a called winner." Names align to a shared left edge in every state of a card.
- **2026-11-03 00:47 UTC.** "Make sure things like this are centered and there should be space between the symbol and the word. And the logo should only exist in one place!! FIX ERRORS LIKE THIS" Centre content in its container, separate touching elements, and show a logo once per page; catch these faults before he sees the build.
- **2026-11-05 20:51 UTC.** "AM and PM is cut off on the right side of governors and other races on the homepage." Text must not clip at the edge of its container.

## Phone and desktop

- **2026-11-02 13:08:35 UTC.** "For phone, I'd prefer a card come up from the bottom." On a phone, detail opens as a card rising from the bottom.
- **2026-11-02 13:21:33 UTC.** "On mobile, when entering the data for a particular state, there should be a back button." A phone view that goes deeper has a back button.
- **2026-11-03 11:33 UTC.** "The back button doesn't fit in with the UI at all. It's like an invented back button. I can't slide up or down because that'll make it seem like I'm trying to reload the page. Is there no more native drawer?" Phone controls should feel native; avoid invented back buttons and swipes that read as pull-to-refresh.
- **2026-11-03 12:37 UTC.** "the experience for both the state pages and candidate races is awful like the cards just suck. I'd like to fully scrap the cards and start from scratch" A pattern that fails on the phone is scrapped and redone, not patched.
- **2026-11-03 12:40 UTC.** "Do whatever page transition you think best towards the end. Only ask if needed." On a delegated phone pattern, decide yourself and ask only if something he has ruled is touched.
- **2026-11-03 12:50 UTC.** "I want the appearance toggle at the top, not the bottom because it becomes invisible. Also if anything falls below the screen in the menu I cannot scroll down to see it. These are all things you should catch yourself." Important controls sit where they stay visible; a menu scrolls whenever its content exceeds the screen, and checks must try the case where content does not fit.
- **2026-11-03 13:13 UTC.** "the appearance change should be a tab switcher but a real component that fits in there, not the —Light —Dark looking thing, as that works vertically but not horizontally." Use a real segmented control, not a list of words laid out sideways.
- **2026-11-03 15:21 UTC.** "it almost cuts off the logo on top because there isn't room between the border and the logo or barely any. More importantly, the left-adjusted elements in the menu have barely any spacing between them and the white or red part of the menu to their left. Like add a bit more natural padding/spacing on the left or shrink the text" Keep clear space between content and any edge or coloured band; prefer more padding to smaller text.
- **2026-11-03 15:39 UTC.** "I'm not sure why the menu button disappears upon a card opening from the bottom." The menu button stays visible when a card opens.
- **2026-11-03 15:39 UTC.** "at least on mobile, on the top there's a little left accent on the time indicator. Needs to be removed. Perhaps that could be a noticeable button." A tappable element should look like a button, without stray accents.
- **2026-11-03 15:39 UTC.** "I would also like to implement skeleton loaders where relevant." Use skeleton loaders where content loads.
- **2026-11-03 16:50 UTC.** "upon completely dismissing a drawer from the bottom, the background remains darker, shadowed, and unselectable. So it basically destroys the functionality of the site. And there are a couple glitches with the shadow upon drawer opening." Check every way of dismissing a drawer; a dim that stays is a blocking fault.
- **2026-11-05 13:35 UTC.** "things drop down below the bottom of the phone so it doesn't work super well because I don't know if scrolling is the right way to reach the rest of the information." On a phone, content must not run past the screen unreachably; redesign the menu so everything is reached.
- **2026-11-05 13:39 UTC.** "… maybe it seems a BIT cluttered now with all the pages? Do they all deserve their own page as-is? Maybe? Maybe not?" Question whether each item deserves its own entry in a menu.
- **2026-11-05 14:27 UTC.** "the transition between the two pages as well as the back button need to be better. The transition should be more like the transitions between pages in the site today, and maybe turn the other four options that are now smaller into buttons or something to make them visually different. Visual separation!!" Match transitions already approved on the site; make different-weight options look different by turning them into buttons.
- **2026-11-05 15:35 UTC.** "I'd like this to occur in independent passes for mobile and desktop, based on extensive research." Research and design the phone and the desktop separately.
- **2026-11-05 12:37 UTC.** "Think about separately how to format this info for mobile." New data displays get their own phone design.
- **2026-11-05 16:41 UTC.** "tapping on the map, like, it selects a district, and that can't happen on mobile. Something on mobile needs to change." A hover or tap-precise interaction that is impossible on touch needs a touch design.
- **2026-11-05 17:06 UTC.** "Governors should not have a semicircle because that makes no sense." Do not offer a view that makes no sense for the data.
- **2026-11-05 19:28 UTC.** "Catch things like this yourself, cut off on mobile." Check every page at phone widths and larger text for cut-off content before he sees it.
- **2026-11-05 20:35–20:36 UTC.** "Identify why they overlap and apply the fix everywhere it should be applied" Find the cause of an overlap and fix it everywhere, by tying the pieces together once in the component.
- **2026-11-05 20:32 UTC.** "Some overlapping things. The pin and the images and maybe more." Pins and images must not overlap or clip each other.
- **2026-11-05 20:45–20:51 UTC.** "the overlapping problem applies literally everywhere... And of course the images are cut off basically everywhere." A fault found once is looked for on every page.
- **2026-11-05 16:13 UTC.** "at least on mobile, the icon is not centered." Check centring on the phone by measurement.
- **2026-11-05 16:23 UTC.** "The icon is still not centered on mobile." A fix that did not fix it is not finished; verify by measurement.
- **2026-11-05 20:58 UTC.** "the icon should have a little bit more space between itself and the dots above it." Give a logo clear space from neighbouring graphics.

## Loading and jumping

- **2026-11-05 18:28 UTC.** "sometimes information loads and then it pushes other info down, so there's a lot of snapping and glitchy moving around, things like that. I want you to be deliberate about every single page, maybe use skeleton loaders." Reserve space for content before it loads, or use still skeletons, on every page.
- **2026-11-05 18:57 UTC.** "And as you know, I hate jumping and I like smooth transitions." Layout jumps are a fault.

## Pages and entrance (sign-in door)

- **2026-11-05 15:23 UTC.** "I want to add user authentication at the start, in the awesome beautiful style of the website. It is the first thing anyone sees, so make it very nice." The first thing anyone sees is made in the site's own style and made well.
- **2026-11-05 18:25 UTC.** "the sign-in page, both on mobile and on desktop, should be really deliberate, large, loud, exciting, etc." The entrance page is large and exciting on both widths.
- **2026-11-05 18:32 UTC.** "there should probably be demonstrations of the features of the site... Keep in mind, the first page should be like visually the most excellent page to ever exist on the site. So it should show election-specific things, but also use real components." The public first page demonstrates what the site does with real components and is visually its best page.
- **2026-11-05 18:35 UTC.** "this should be the most deliberate part of the app ever." Research how the site's purpose leads to the entrance design before choosing what it shows.
- **2026-11-05 19:09 UTC.** "one of the primary goals is actually coolness. So certainly I don't want just plain screenshots of the site, or even necessarily exactly the site's components." The entrance is not a screenshot of the site; it is showpieces in the site's style, from the same true data.
- **2026-11-05 20:58 UTC.** "be very deliberate with the buttons, passcode, and first name, and enter, and anything else." The entrance's form controls are designed with care.
- **2026-11-05 21:00 UTC.** "I think the background should have some sort of effect." The entrance has a background effect.
- **2026-11-05 17:35 UTC.** "it should be far more special looking, and also, like, it looks very, very simple right now. Like, it's just the most simple possible buttons, lines, very simple text." Plain buttons, lines and text read as unfinished; a special element should look special.
- **2026-11-05 17:35 UTC.** "it should draw attention to itself as well, but be easily dismissible so it's not annoying." A prompt draws attention but closes in one tap.
- **2026-11-05 20:49 UTC.** "set a thread to reorganize each of the candidate pages or the district pages" Each kind of detail page gets its own considered layout.

## Search, menus and navigation

- **2026-11-02 13:21:33 UTC.** "I don't want the menu on top. Like that. I would prefer a menu that like a pop-out menu from the side. Like maybe similar to the Claude or ChatGPT or Gemini menus." Prefer a side pop-out menu in the manner of the well-known chat apps over a top menu (superseded later by the reveal; the preference for a slide-out remained).
- **2026-11-02 14:40:36 UTC.** "the search feature should be able to search anything relevant" Search covers everything the site holds.
- **2026-11-02 20:40 UTC.** "why has nothing changed about the menu on desktop? Or the search?" Menu and search are judged on desktop as well as phone.
- **2026-11-02 20:45 UTC.** "the search kind of sucks because the info is like disparate in different places." Search results are one list, not scattered.
- **2026-11-03 12:41 UTC.** "More and more I'm starting to think I prefer that over the persistent bottom menu, for both mobile and desktop." He prefers a reveal menu (page slides aside) to a persistent bottom bar.
- **2026-11-03 12:50 UTC.** "I prefer the concept of the reveal sidebar, but far more work needs to be done." Preference for the reveal sidebar; it needs craft.
- **2026-11-03 14:23 UTC.** "I'd like to see another option with the reveal that has the white-orange little panes, which I think is 2.0." He wants two sourced options to compare.
- **2026-11-03 14:25 UTC.** "make sure the newest nav menu... works in all modes and that it is organized well!! Check and test it!" A menu works in every scheme and size and is organized well before he sees it.
- **2026-11-05 15:23 UTC.** "New preview of the nav menu is perfect." The approved menu: reveal, navy, red and white, with its order and buttons as shipped.
- **2026-11-05 19:00 UTC.** "the overlay seems to have been ignored. Like some of the information might be wrong or outdated or just not kept up with what we've been doing." A search index and its labels are re-audited against the current site.

## Process: how design is done and checked

- **2026-11-05 22:27 UTC.** "I don't know how to decide yet, so I'll wait for full sample sign in pages put together to decide!" Show whole worked examples to choose between, not part-by-part shortlists.
- **2026-11-02 13:26:51 UTC.** "keep in mind that adding these features requires very, very deliberate consideration of where I would want to see the features, where would be the most useful, etc." Before adding a feature, decide deliberately where it is most useful.
- **2026-11-02 13:17:57 UTC.** "I want you to be deliberate about how special the website is, right? Like, it should show things as beautifully and as coolly as it possibly can." Aim for a special site, not an adequate one.
- **2026-11-02 14:40:36 UTC.** "Let's first review whatever plan you or a subagent comes up with that suggests similar kinds of changes." He reviews a plan of principle-driven changes before they are built.
- **2026-11-02 15:48 UTC.** "I don't want to sacrifice nice components or my own review because time has expired." Time pressure never cuts component quality or his review.
- **2026-11-02 21:29 UTC.** "think of how I can interact as LITTle as possible for this" Where a step needs his hands, find the way with the fewest first.
- **2026-11-02 21:42 UTC.** "as little, as I have to do, and as easy as you could possibly make it for me to know what I have to do... In that page, and I do not want extra text." Show him exactly his decisions, one line each, without extra text.
- **2026-11-02 14:56:54 UTC.** "I basically wanna watch the live most updated version of the page itself and watch it update autonomously as new pushes arrive" Give him a live preview hub of all pages being made.
- **2026-11-03 15:53 UTC.** "we need to imbue the principles behind the design, all of the ideas behind ALL of the changes I've requested in the history of this project, and I want it to look for issues based on similar logic." A review agent receives the principles and every past request, and looks for issues by the same logic.
- **2026-11-03 21:53 UTC.** "functional errors fully destroy the site." A functional fault outranks any appearance fix.
- **2026-11-03 22:01 UTC.** "I want it visually tested before I start heavily using the site" Visual testing on the deployed site, on phone and desktop, in both schemes, precedes his heavy use.
- **2026-11-03 23:08 UTC.** "try to get at the heart of what I'm getting. I want a response in the coordinator chat about what you think my true goal is here, and then for you to work in the background." State his underlying goal back to him, then work.
- **2026-11-05 12:20 UTC.** "I want to be very clear about what the math is, what the formula is behind the information that's shown. And then I want you to rethink the visual hierarchy of the information that's there. But most importantly is the data." Set out the formula plainly with a worked example; the data's soundness comes before visual polish.
- **2026-11-05 12:37 UTC.** "Be VERY specific and deliberate with what you implement, making sure to consider all possible forms of user interface and interaction to implement the BEST possible solution." Consider every possible form of interface and interaction before choosing.
- **2026-11-05 13:50 UTC.** "You can send off sub-agents to do research, sub-agents to make considerations or think of different ideas, like based on the principles of the changes I've made." Use subagents to research and generate ideas, guided by his past principles.
- **2026-11-05 14:27 UTC.** "Do not deploy yet but let me know concisely when the new preview is ready" Preview first and tell him briefly.
- **2026-11-05 15:37 UTC.** "Send a thread to do that." Specialised fixes go to their own worker.
- **2026-11-05 16:16 UTC.** "You could maybe set another thread to look for things like that in the site, and I want them fully removed." When he names one instance of a fault, send a worker to find all instances.
- **2026-11-05 18:59 UTC.** "where someone doesn't have a photo, I'd like a stand-in so there's not just white space." A missing image gets a plainly non-likeness stand-in, never blank space.
- **2026-11-05 18:59 UTC.** "it's really weird when there's just one photo and then two blank areas in the same race." Items shown side by side look consistent with each other.
- **2026-11-05 15:37 UTC.** "I want the photos more standardized. Ideally just the heads and no backgrounds, but at least the same background if not." Portraits share one crop and background.
- **2026-11-05 22:09 UTC.** "Run all redesigners on max effort" Design workers run at maximum effort.

## Markets and data displays (visual lessons)

- **2026-11-05 12:37 UTC.** "next to as many races or anything as possible, well thought-out data displayed about Kalshi or other bets, maybe at different points in time?" Place relevant secondary data beside the main item, over time where useful.
- **2026-11-05 16:15 UTC.** "I'm also thinking about having popovers with a small version of a candidate's profile? In the nice style of details.so and the rest of the site" A small profile popover on a name or face, in the library's style.
- **2026-11-05 20:47 UTC.** "I don't just want to see surprises on the surprise specific page. So for example, if I click on a Senate race, I want to see how surprising the outcome was." A summary insight also appears at the item it concerns.
- **2026-11-05 20:49 UTC.** "the text polls close, CNN call seems to overlap with other lines." Lines of small text must not overlap in tight rows.
- **2026-11-05 03:54 UTC.** "very deliberately well implemented and with a nice visual hierarchy, like on the US or state maps or whatever" New data layers on maps are built with the same hierarchy.

## Left out

Rulings with no design lesson, or only elections, data, money, accounts or deadlines.

- 2026-11-01. Inventing district shapes (data sourcing).
- 2026-11-02 00:05 UTC. A census of the field was premature.
- 2026-11-02 03:15 UTC. Settled scope (open to anyone, free accounts, ballot measures, television).
- 2026-11-02 03:29 UTC. "The law is ratified."
- 2026-11-02 03:58 UTC. Writing to AP and DDHQ for prices.
- 2026-11-02 14:43:42 UTC. Opus versus Fable for the project.
- 2026-11-02 14:49:34 UTC. Cost of a model is zero.
- 2026-11-02 14:53:01 UTC. Approval of the plan; the logo left alone.
- 2026-11-02 15:19:58 UTC. Buying the details.so max plan.
- 2026-11-02 17:03 UTC. Downloading the rest of the details.so catalogue.
- 2026-11-02 20:50 UTC. "I trust your judgment for all three."
- 2026-11-02 21:34 UTC. The Blob store.
- 2026-11-02 23:51 UTC. The dock menu choice (card choice, later superseded).
- 2026-11-02 23:52 UTC. Merges to main.
- 2026-11-03 00:09 UTC. Tell him when components reach main.
- 2026-11-03 11:10 UTC. Vercel credits.
- 2026-11-03 12:31 UTC. Other desks in production.
- 2026-11-03 14:22 UTC. "Is the new nav menu being implemented?"
- 2026-11-03 15:47 UTC. Tonight's spend.
- 2026-11-03 19:31 UTC. ChatGPT's first-pass review.
- 2026-11-03 21:08 UTC. Freeze lifted; pushes to main.
- 2026-11-03 21:11 UTC. Sharing the site widely.
- 2026-11-03 22:24 and 22:27 UTC. Desks' calls and the Bluesky reader.
- 2026-11-03 22:31 UTC. The AI reader and its $199 cap.
- 2026-11-04 00:05 UTC. Call alert form (card choice).
- 2026-11-04 00:07 UTC. A banner for every call; call times.
- 2026-11-04 00:10 UTC. AI reader token use.
- 2026-11-04 00:12 and 00:13 UTC. A desk's call colouring the race.
- 2026-11-04 00:14 UTC. Build in parallel on election night.
- 2026-11-04 00:45 to 01:12 UTC. Feed checking, accuracy, civicAPI down, NYT counts.
- 2026-11-04 01:56 to 02:35 UTC. Merging, partial sums, other sites' numbers, AP direct, DDHQ, Michigan and Texas.
- 2026-11-04 03:05 and 03:13 UTC. Chamber-control calls; NY county sums.
- 2026-11-04 03:39 to 03:46 UTC. Stale races, civicAPI, his Mac, odds and dial, official feeds.
- 2026-11-04 11:21, 12:01 and 12:15 UTC. Standing down; Vercel charges; the updater.
- 2026-11-04 15:10 UTC. The updater fades out.
- 2026-11-04 16:32 UTC. Protecting old deployment links.
- 2026-11-04 18:41 UTC. Repeated call-changed banner and inflated update counts (data truth).
- 2026-11-05 14:13 UTC. Pennsylvania test data.
- 2026-11-05 14:18 UTC. Photos under fair use; "Make more changes like the ones in suggestinf".
- 2026-11-05 15:33 UTC. How guests get in.
- 2026-11-05 16:11 UTC. The passcode.
- 2026-11-05 16:29 UTC. One-time invite codes in Supabase.
- 2026-11-05 16:31 UTC. A private dev page.
- 2026-11-05 16:35 UTC. Keys added (the variables).
- 2026-11-05 16:44 UTC. The verdicts on the previews (specific to those items).
- 2026-11-05 19:02 UTC. The governors' "no votes".
- 2026-11-05 19:37 UTC. The task board.
- 2026-11-05 19:45 UTC. Photo requests approved.
- 2026-11-05 20:30 UTC. BallotReady.
- 2026-11-05 20:37 to 20:39 UTC. The Before tab on the bar; the door preview link (specific).
- 2026-11-05 22:07 UTC. Mobbin deep mode (tool usage).
- 2026-11-05 14:13 to 15:39 UTC. "deterministically reformatted" profile remark folded into data/process; not separately kept.
