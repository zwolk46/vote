# Cold readings of the explainer, "How the figure is worked out" (brief X2)

Every reading is recorded verbatim. Each reader was a fresh Sonnet 5.5 subagent at xhigh effort. None saw the briefs, the model or this repository; each saw only screenshots of the page. *Reason:* the maker's test is a non-technical person who understands from the page alone (brief X2, "The test before he sees it"), and a reader who has seen the model cannot stand in for one.

The two versions show the same pictures and the same words. A scrolls them past a held picture; B steps through them with a tap. The screenshots are B's steps, one per step, at 390 px, in light. One set of readings therefore covers both versions; what differs between them is pace and motion, which a screenshot cannot show.

## Round 1, reader 1: the visuals alone (2026-11-07)

**What was read.** Commit d200f58 on `claude/project-thread-ozfwbq-explainer`, with its canvas labels kept inside the box at large text. There were 22 steps, with every sentence removed by hiding each element marked `data-sentence`. Those elements are the source folds and the last line on what is set aside. Labels, figures, headings, axes and the keys of marks were kept, as the amended brief asks (04:35).

**The reader's instructions, as given.**

> You are a reader, not an assistant. You are an ordinary adult with no background in statistics, mathematics or economics. You have never studied probability. You are reading a web page on your phone.
>
> The page is shown to you as 22 screenshots, one for each step, in order. On the phone you move from one step to the next by tapping "Next". Some of the page's text has been removed on purpose; read only what you see. Look at each screenshot with the Read tool, in this order, and look closely at the pictures, their labels and the small key of marks under each picture: [the 22 paths]
>
> Do not open any other file, search anything, or use any knowledge beyond what an ordinary person would bring. Do not look anything up. Answer only from the screenshots.
>
> When you have looked at all 22, answer these five questions in your own words, as you would explain them to a friend, as best you can. If you cannot tell, or you are guessing, say so plainly; an honest "I couldn't tell" is more useful than a confident guess.
>
> 1. What does "the chance my vote matters" mean here?
> 2. Why does a tie matter, and why is a tie counted as half?
> 3. Why does a big, lopsided race give a smaller chance than a small, close one?
> 4. What are the "break-even stakes" (the least the result must be worth to you), and where does that figure come from?
> 5. Why is the chance for the presidency so small?
>
> Then, separately: which steps (by number) did you not understand, or understand only partly, and what about each one confused you? Be specific about the picture: which mark, label or change you could not read.
>
> Reply with your answers only, in plain prose, numbered as above.

**The reading, verbatim.**

> I looked at all 22 screenshots in order and answer only from what I saw.
>
> 1. "The chance my vote matters" seems to mean the chance that my single ballot is the one that decides who wins. That only happens if everyone else is exactly tied, or my side is exactly one vote short. For the 2,000-voter town race the page says this is "1 in 468". I read that as: imagine the same election happening 468 times, and in about one of those my ballot makes the difference (the dot with the ring around it on steps 10 to 14).
>
> 2. A tie matters because a tie is one of the two situations where my ballot changes the result. If my side is one vote short, my vote turns a loss into a tie. If it is already tied, my vote turns a tie into a win. The page says a tie "goes to a lot", which I took to mean a coin-flip-style draw. So a tie is worth half a win to my side. The two cases are each worth half, and "half + half" makes "one change" (steps 2 and 3, the half-filled circles and the blue halves). I think I follow this. I'm a bit unsure why the filled bar on the bell curve is shorter than the hollow one, though I'm guessing that is the "half".
>
> 3. Looking at the pictures (steps 4 to 9), the bell curve shows how likely each possible result is. A tie sits at 50-50 in the middle. If the race is lopsided, the 50-50 spot is out on the thin edge of the curve, so a tie is rare. A 52-48 forecast gives 1 in 468, 56-44 gives 1 in 1,183, and 60-40 gives 1 in 7,563. A bigger race behaves the same way. With 20,000 voters the chance is 1 in 4,558, and with 200,000 voters it is 1 in 45,460. The curve gets flatter and the 50-50 slice gets thinner. I can see that it happens. I only half see why: with more voters, an exact tie seems like hitting one number out of a much bigger set. The "Less sure" step (step 9) surprised me. The curve is wider and the chance is smaller (1 in 836), when I would have guessed it would be larger.
>
> 4. The break-even stakes seem to be "your cost × N", where the chance is 1 in N (step 20). For the town race it is $8.87 × 468 = $4,150. If the result is worth more than that to me, voting pays. If it is worth less, it doesn't (steps 16 and 17, with $1,000 and $10,000 as examples). The 468 comes from the bell-curve chance. The $8.87 is the cost of one trip to vote, but I could not tell where $8.87 comes from or what is in it (time, travel, something else). No label I could see says so, and the "Source" links are only links. The presidency version is 10 million × $8.87, about $89 million (step 18). Step 19 spreads that over 300 million people to get 30 cents each. I guess the point is that the result would have to be worth about 30 cents to every American. I'm not sure that is what it means.
>
> 5. The presidency chance is tiny because there are two hurdles, and both involve huge numbers of voters. First my ballot has to decide my state, which is about 1 in 1.4 million for Pennsylvania in 2024 (step 12). Second, that state has to be the one that decides the "College", which I took to be the Electoral College. That happens in 19 of 100 of those runs (step 13). Together that gives about 1 in 7.5 million (step 14). For the closest states in 2008 the page says 1 in 10 million (step 11). I understand the idea that it is far smaller. I can't see the arithmetic myself, and I'm guessing you combine the two numbers by multiplying their chances.
>
> Steps I did not understand, or understood only partly:
>
> - Step 1: The two grids look almost the same, with 1,040 to 960 versus 1,039 to 960. My side wins in both. I could see the ringed dot on the left and the empty ring on the right. I could not tell what the picture is meant to show, because my ballot doesn't change the winner here.
> - Step 2: The row of circles from -3 to +3 labelled "your side's lead among everyone else" took me a while. I had to work out that "everyone else" leaves me out. The box around -1 and 0, and the black, gray and half-black circles, only made sense after step 3.
> - Step 3: The blue half-circles and the single blue circle below them. I guessed the lone circle is the two halves added together.
> - Step 4: I couldn't tell what the tall hollow bar versus the short filled bar means, even with the key. I also couldn't tell what "give or take 4" means, or why the peak is right of 50-50. I couldn't check where "1 in 468" comes from. It is just stated.
> - Step 6: At 200,000 voters the curve is a flat line and I could not see any bar. I could only read the number.
> - Step 9: Why a wider curve (less sure) gives a smaller chance. I can't explain it.
> - Step 10: What "one run of the election" means. I guessed it means "the same election held again". I also couldn't count the dots to check 468.
> - Step 11: The dots are too tiny to see, so I only got the idea from the numbers. I also wasn't told why the presidency is quoted as 1 in 10 million (2008) here but 1 in 7.5 million (Pennsylvania 2024) later, or what "closest states" means.
> - Step 14: The square marked "step one's 1.4 million" sits inside the bigger grid. It looks like a small piece inside a bigger whole, which seemed backwards to me. I got the result from the text, not the picture.
> - Step 15: Where $8.87 comes from. This is my biggest gap. I also had to think about "a trip in every run". I took it to mean I make the trip every time, but only one of the 468 runs is decided by my ballot.
> - Step 19: Why the $89 million is divided by 300 million people, and what "counting what it is worth to everyone" means. It is not explained on the screen as far as I can see.
> - Step 20: The number line jumps from $1 to $1,000 to $1 million to $1 billion, and I didn't notice at first that each step is 1,000 times bigger. I understood the "× 468" and "× 10 million" arrows only because of the text.
> - Steps 21 and 22: I mostly did not understand these. "Each race repays a share of the trip" is unclear. I don't know where 51%, 25% and 29% come from, or why a total of 105% means "It pays". It also seems odd that the President has the biggest share here when the presidency "does not pay" on step 18. I'd guess the idea is that one trip covers three races, so the costs are shared. I'm only guessing.

### What the reading found, and what was changed

The reader answered all five questions from the pictures. It read the chance as one run in N, the tie and the one-short count as half and half, the curve falling with more voters and off even, the break-even stakes as cost × N against what the result is worth, and the presidency as two steps. These steps failed or were weak:

- **Step 1 showed nothing changing.** The two worlds now have a second state: a close run, 1,000 to 1,000 against 999 to 1,000, where the winners differ. Each world names its winner under its count.
- **The curve's two bars (the outline and its filled half) were not read.** The marks are now labelled on the picture itself, the outline "a tie or one short" and the filled half with the chance. The forecast's centre is marked with its share where it stands apart from 50–50.
- **Where $8.87 comes from** (the reader's "biggest gap"). The step that brings in the trips now shows it: 14 minutes at $38 an hour.
- **Why the $89 million is shared by 300 million people.** That step is now the same seesaw. One end holds the 10 million trips, the other the 300 million people's stakes at 30¢ each, and the two weigh the same.
- **The ballot's percentages** (not understood) are replaced by the same seesaw, one trip against what each race repays of it. The example worths are now ones that do not pay alone: the town race at $1,000, as on the seesaw that did not pay. The races arrive one at a time, and the beam tips only when all three are on it.
- **Step 14's inner square read as backwards**, so it was removed. The field's growth from 1.4 million to 7.5 million carries the step.

## Round 1, readers 2 and 3: the page with its words (2026-11-07)

**What was read.** Commit beb1c9e, after the changes above. There were 24 steps, each as a screenshot at 390 px in light with its words. Each reader also had the page's text, step by step, with every step's "Source" opened (`page-text.txt`, taken from the page). The canvas labels are in the screenshots only.

**Reader 2's instructions**, as given: "You are a reader, not an assistant. You have a broad education (you read the news, you went to university in a subject that was not mathematical) but you have no statistics: you have never studied probability or economics. You are reading a web page on your phone." The rest was as for reader 1, with the 24 screenshots and the page's text, and the same five questions and the question about the steps not understood.

**Reader 3's instructions**, as given: "You are a reader, not an assistant. You are a total layperson: you have no technical understanding at all. You left school early and do not use numbers beyond everyday shopping. You do not know what a cost-benefit analysis is. You have never weighed a small chance of a large gain against a sure cost, and nobody has ever told you that such a weighing is how one decides whether something "pays". Read as that person would: do not supply knowledge they would not have." The rest was as for reader 2, with a sixth question: "6. Why can paying a small, sure cost for a tiny chance of a large gain pay in one race and not in another?"

### Reader 2 (broad education, no statistics), verbatim

> 1. "The chance my vote matters" is not the chance my side wins, and it is not the chance my ballot gets counted. It is the chance that everyone else's votes land so close that my one ballot decides the winner. That happens in two cases. Either the others are exactly tied, or my side is behind by exactly one vote, so my ballot makes it a tie. The page puts a number on this by forecasting the whole race and asking how likely it is that the others end up right on that knife-edge. In the town example, "1 in 468" means this. Picture the election run 468 times, and in about one of those runs my ballot is the deciding one. The last screen says it is the only thing weighed. Duty and having my say are set aside.
>
> 2. A tie matters because it is the only place where one ballot changes anything. If the others are tied, my ballot gives my side the win. If my side is one short, my ballot turns a loss into a tie. A tie is settled by lot, which I take to mean a coin toss or drawing straws. So in the tied case my side would have won half the time anyway, and my ballot only lifts it from half a chance to a sure win. That is half a change. In the one-short case my ballot lifts it from no chance to half a chance. That is also half a change. The two halves together make the "one change", which is the "Half + half" screen. From the step 5 picture I read the 1 in 468 as the figure after halving. The outlined "tie or one short" box is the whole slice, and the dark blue bar inside it is about half of that.
>
> 3. The page gives two reasons, and I am partly inferring the "why" from the pictures because it is barely said in words.
> - More voters. With 2,000 voters it is 1 in 468. With 20,000 it is 1 in 4,558, and with 200,000 it is 1 in 45,460. The curve gets flatter and lower. I take that to mean the forecast is spread over many more possible final tallies, and a tie needs one exact tally. Ten times the voters gives roughly ten times less chance.
> - Lopsided. At a 52–48 forecast the tie sits near the hump of the curve. At 56–44 it sits on the slope, and the chance falls to 1 in 1,183. At 60–40 it sits almost at the foot, at 1 in 7,563. The expected result is far from the 50–50 line, so a tie would be a freak outcome.
>
> 4. The break-even stakes are the least the result must be worth to me before voting is worth my trouble. The figure is my cost of voting multiplied by N, where my chance is 1 in N. The logic is that I would have to make N trips to the polls to get one run where my ballot decides. In the town race that is 468 × $8.87 = $4,150. For the presidency, with N at 10 million, it is about $89 million. The $8.87 is 14 minutes at the polls, the median from a study by Chen, Haggag, Pope and Rohla (2016 data), at $38 an hour from the Bureau of Labor Statistics (October 2026, preliminary). N comes from the page's "model". The town's 1 in 468 is a made-up "stylised" example. The presidency's 10 million is from Gelman, Silver and Edlin (2012), and Pennsylvania's figures are from the model's own forecast. What the result is worth to me is my own call. The $1,000, $10,000 and $50 million are labelled examples, so the "pays / does not pay" verdicts depend on invented numbers. I could not tell what "the model" actually is, who built it, or how it was checked. The sources only point to things like "model §2" and "model/math/common.py".
>
> 5. For the presidency, two small chances are multiplied. First, millions of people vote in my state, so my ballot would have to be the exact tie-breaker there. For Pennsylvania in 2024 that is 1 in 1.4 million. Second, that state would then have to be the one that decides the whole Electoral College, which the page puts at about 19 in 100 of those cases. Together that is 1 in 7.5 million. The separate 2008 "closest states" figure of about 1 in 10 million says the same thing. Big electorates make an exact tie very unlikely, and then the state has to matter nationally as well.
>
> Steps I did not understand, or only partly:
>
> Step 3. I could read the half-dark, half-grey circle as "a tie by lot". I could not at first read "your side's lead among everyone else" along the bottom. The minus and plus signs are very faint, and I did not see why only the −1 and 0 columns sit in the box. I pieced it together later. There is also a big blank gap in the middle of the screen.
>
> Step 4. I could not tell what the blue halves mean. Blue is on the left half of the −1 circle and the right half of the 0 circle. A single blue circle floats below with no label and no arrow linking it to the others. I got "half + half = one" mostly from the words.
>
> Step 5. I did not know what the curve is. There is no vertical scale. Nothing on this screen says that its height is the chance of an exact tally. That is only in the Source link opened at step 6. "Give or take 4" is never explained. I guessed it is the forecast's uncertainty.
>
> Steps 6 and 7. At 200,000 voters the curve is a flat line and the bar cannot be seen at all. Only the number "1 in 45,460" tells me anything. The page also never says why more voters makes the curve lower.
>
> Step 10. "Less sure" (give or take 8) gives a smaller chance, 1 in 836 against 1 in 468. I would have guessed the opposite, that being less sure makes a tie more plausible. The picture shows a wider, flatter curve, but nothing explains why that lowers the tie.
>
> Step 12. The dots are so tiny that they look like grey haze, and I cannot count or read them. The key says each dot is "one run of the election", but the caption says "millions of voters", so I was unsure what a dot is. "Closest states, 2008" is not explained. I guess it means the best case for a voter.
>
> Steps 13 and 15. The two dot squares look identical in size, although one is 1 in 1.4 million and the other 1 in 7.5 million. The picture does not show that one is five times rarer.
>
> Steps 12, 15 and 19. The page uses 10 million (2008, from a paper), then 7.5 million (Pennsylvania 2024, from the model), then goes back to 10 million at step 19. I did not know why it switches or which one is "the" figure.
>
> Step 14. The step never says "Electoral College". I only knew "the College" from my own general knowledge. The key text "the state decides the College; it does not" reads oddly. I could count the 19 blue dots out of 100. Why it is only 19 is not explained.
>
> Step 20. The key says "a million people, each at 30¢", but the label says "300 million × 30¢". I guessed each black dot is a million people. The step also quietly switches from what the result is worth to me to what it is worth to everyone. That is a different point of view, and the page does not announce it.
>
> Step 21. The line from $1 to $1 billion is evenly spaced, but each tick is 1,000 times the last. I worked out that it is a stretched scale, but the page does not say so. I was also unsure where the two arrows start and end.
>
> Steps 22 to 24. I understood these. The one-in-180,000 House chance and the 1898–1992 years appear only in the Source text, not on the screen. The House bar (black) and the Town bar (dark slate) are hard to tell apart.
>
> Step 2. The heading says "Different winners". But a tie by lot is not a sure win for my side, so it is only half true until steps 3 and 4.
>
> Source texts, throughout. Phrases like "normal curve", "exact sums by its code", "model §5" and "law 2c" meant nothing to me.

### Reader 3 (total layperson), verbatim

> 1. "The chance my vote matters" means the chance that my one ballot is the one that decides who wins. Steps 1 and 2 show two sets of dots, one with my ballot counted and one with it not counted. In step 1 the same side wins either way, so my ballot made no difference. In step 2 the race is so close that it comes out differently depending on my ballot. The page puts a number on this: "1 in 468" for the small town race. I read that as "if the same race happened 468 times, my ballot would be the deciding one about once". Step 11 shows 468 dots with one circled, and the page calls each dot "one run of the election". I'm guessing "run" means one go at the election, because the page never says so.
>
> 2. A tie matters because it's the only time my one vote changes anything. Step 3 shows a row of circles from -3 to +3 for "your side's lead among everyone else". Outside the boxed pair of columns, the counted and not-counted rows look the same, so my vote changes nothing there. Inside the box, there are two cases. If everyone else is tied, my vote puts my side ahead. If my side is one short, my vote makes it a tie. A tie is settled "by lot". I think that means drawing straws or tossing a coin, but the page never says so. Since my side would have won half of those draws anyway, my vote only adds half a win in each of the two cases. That's why it says "Half + half" in step 4. I follow that part. I don't really follow how the page then turns those halves into the final figure. It says the chance is "half the chance of the two counts", and that went over my head.
>
> 3. I can see this in the pictures, but the page doesn't say why in words. Steps 5 to 10 show a hill shape with a small blue bar at the middle (50-50). The bar is the chance of a tie, and the filled part is my share of it. With more voters (2,000, then 20,000, then 200,000) the hill gets flatter and the number gets bigger: 1 in 468, then 1 in 4,558, then 1 in 45,460. Further from even (56-44, then 60-40) the hill slides away from the middle and the bar sits low on its side. The number goes to 1 in 1,183, then 1 in 7,563. My guess is that more voters means more ways for the count to come out, so landing exactly on a tie is rarer. A lopsided race makes a tie unlikely in the first place. That is my guess from the pictures, not something the page told me. "Less sure" (step 10) also made the number worse, 1 in 836. I didn't expect that, and I can't tell why. I only see that the hill is wider.
>
> 4. The page never says "break-even stakes". Its words are "the least the result must be worth to you". I take that to mean the smallest amount the winning would have to be worth to me for the trip to be worth making. The page's rule is "your cost × N", where the chance is "1 in N". The cost is $8.87 for a trip to vote (step 16). That is 14 minutes at the polls at $38 an hour. The 14 minutes is credited to a study I don't know. The $38 is credited to "BLS", which I can't read, so I don't know whose hourly pay it is. The "× N" part comes from step 16. To be the deciding vote once, I'd have to make 468 trips. 468 × $8.87 is about $4,150, so the result would have to be worth at least that. I mostly follow the seesaws: $1,000 is too little and $10,000 is enough. I don't see why I'd count 468 trips when I only vote once, and I just went along with it. Also, nothing on the page tells me what a result is worth to me. It says "yours to say" and gives $1,000 and $10,000 as made-up examples.
>
> 5. The page gives two reasons, and the second one confused me. First, my state has millions of voters, so being the one who flips my state is rare: 1 in 1.4 million for Pennsylvania (step 13). That fits what I saw with more voters. Second, even if I flip my state, it only decides the whole country's result about 19 times in 100 (step 14). Both have to happen, so it comes to 1 in 7.5 million (step 15). Elsewhere the page says 1 in 10 million for the closest states in 2008 (step 12), a different year and a different figure. I don't know why my state would decide only 19 in 100 times, because the page doesn't say.
>
> 6. It depends on how small the chance is compared with what the result is worth to me. For the town race, with a chance of 1 in 468, I'd need the result to be worth only about $4,150. At $10,000 it pays and at $1,000 it doesn't (steps 17 and 18). For the presidency, with a chance of 1 in 10 million, I'd need it to be worth $89 million. Against $10,000 it doesn't pay (step 19). The last steps (22 to 24) add something else. One trip votes in every race at once, so each race pays back a little of the $8.87: $5.00 for the president, $2.22 for the House and $2.14 for the town, together $9.36 against $8.87. So it pays together even though none pays alone. All the dollar worths there ($50 million, $400,000, $1,000) are made-up examples. The page also says it counts only the chance of changing who wins, and sets aside duty and having your say.
>
> Steps I didn't understand, or only partly:
>
> - Step 1: The two sets of dots look almost identical. I could read "1,040 to 960" against "1,039 to 960" but couldn't see any difference in the pictures.
> - Step 2: It says "Different winners". But one side is "a tie: by lot", so I don't see how a tie gives a different winner. The phrase "by lot" also looks like "a lot", meaning many.
> - Step 3: Only partly. The minus signs on -3, -2, -1 and the label "your side's lead among everyone else" were hard for me. Why the half-filled circle sits in different places in the two rows wasn't clear, though I guessed it from the box.
> - Step 4: Only partly. The lone blue circle under the grid has no arrow or label connecting it to anything.
> - Steps 5 to 10: There is no up-and-down scale on the hill, so I never knew what its height means. "Give or take 4" and "give or take 8" are unexplained. In step 7 the hill is a flat line and I couldn't see the bar at all. In step 9 the bar is a speck. The source links mention a "normal curve" and "exact sums by its code", which meant nothing to me.
> - Step 11: Only partly. The dots were voters in step 1 and are now "runs of the election", with no warning that their meaning changed.
> - Step 12: The dots are so many they blur into grey. The caption says "millions of voters" but the key says each dot is a run, so I couldn't tell which it is.
> - Step 14: "The College" and "electoral votes" are never explained. I thought of a school. I also couldn't tell why the figure is 19 in 100.
> - Step 15: The grid looks exactly the same as in step 13, so I couldn't see how combining two things makes it rarer. I only had the words.
> - Step 16: Only partly. I didn't see why one trip is counted in every run.
> - Steps 17 to 19: The seesaw is easy to read. Not knowing what the result is worth to me is not. I don't know how a town race or the presidency could be "worth $1,000" to me.
> - Step 20: I did not understand this step. It suddenly switches to what the result is worth to everyone, "30¢ each". I couldn't tell why other people's gain counts for my trip, or what "a round figure" is for. The key says "a million people, each at 30¢" but the seesaw says "300 million × 30¢". I wasn't sure what a level seesaw means here.
> - Step 21: Only partly. "N" is a letter standing in for a number. The line from $1 to $1,000 to $1 million to $1 billion jumps by a thousand each time, and the two arrows (× 468 and × 10 million) sit close together. It was hard to read the dots and prices along the line.
> - Steps 22 to 24: Only partly. Why it's now "÷ N" when it was "× N" before wasn't clear. "Repays" is never explained. The House ($2.22) and town ($2.14) shares appear only in the Source text, not in the pictures. The black, dark grey and grey blocks in step 24 look very alike.
> - The Source links: "model §2", "law 2c", file names, "BLS" and the researchers' names meant nothing to me.

### What readers 2 and 3 found, and what was changed

Both readers answered every question rightly, the layperson's sixth too. Their partial misses were these, and each was met where a picture or a word could meet it:

- **"By lot" read as "a lot"** (reader 3). Every mark and heading now says "a coin toss": the key "a tie: a coin toss decides", the heading "A tie goes to a coin toss". The source says "settled by lot (a coin toss, or straws drawn)".
- **"Different winners" when one side only ties** (both). The figure now reads "Different results", and its sub "a coin toss against a loss".
- **The axis words were hard** (both). They are now "your side's lead, not counting you". They are drawn over the dashed paths of step 4, so the paths pass behind them.
- **The lone circle in step 4 had no link or label** (both). Dashed paths now run from the two halves down to it. It is named "= one change" beside it where it fits, and in the key ("what your ballot changes").
- **The curve had no scale, and its height meant nothing** (both). An arrow up the left side is named "how likely", and the key names the curve "how likely each count is".
- **"Give or take" was never shown** (both). It is now a bracket across the curve, from one give or take below the forecast's centre to one above, named in the key ("give or take: how wide the forecast is"). In the "Less sure" step the bracket doubles and the curve flattens.
- **Why more voters, or less sureness, lowers the chance** (both). From step 6 on, the first forecast stays on the picture as a dashed curve, named in the key ("before: 2,000 voters, 52–48, give or take 4"). Each change is seen against it: the same curve spread over more counts, or wider, stands lower at 50–50.
- **The bar was invisible at 200,000 voters** (both). Where the bar is under 5 pixels, a mark under the axis points at it.
- **Step 12's sub, "millions of voters", made the dots read as voters** (both). It is now "the closest states, where millions vote". The key still says each dot is one run.
- **Steps 13 and 15 looked the same size** (both). Each field is now sized by its count of runs. Step one's 1.4 million fills less than half the width of both steps' 7.5 million.
- **"The College" was unexplained** (both). The heading and the key now say "Electoral College". Why it is 19 in 100 is left to the source: it is the share of runs where the other states leave the College close enough. A picture of it would be a third stage, which the brief does not ask for.
- **Why count 468 trips when I vote once** (reader 3). The step's heading is now "In 468 runs, 468 trips".
- **Step 20, the share** (both). The key now says "each dot: a million people", which matches the label "300 million × 30¢". A label over the picture says "level: they weigh the same". The sub now says what the round figure is: "(a round figure for the country)".
- **Steps 22 to 24, the ballot** (both). The keys say "shared over 180,000 trips" in place of "÷ 180,000". The trip is now an open box and the races solid blocks. The three colours are now apart: accent, ink and light grey. Each block carries its dollars ($5.00, $2.22, $2.14) where they fit inside it.
- **The sources' jargon** (both). The sources now say "the site's model, section 2" in place of "model §2" and name no files. "Law 2c" is gone, and "Bureau of Labor Statistics" is spelled out. "Normal curve" and "exact sums by its code" are now "a bell curve" and "worked out exactly by its own code".
- **Left as they are.**
  - The switch between 2008's 10 million and Pennsylvania 2024's 7.5 million. The brief asks for D1's figures in the two stages and the 2008 closest states for the comparison. Each step names its race and year.
  - The scale of dollars in step 21. It was read rightly by both, with effort. Its marks are the figures the reader has just seen, and a second picture of the same idea would add more than it clears.
  - The faint minus signs. They are the muted colour of the counts outside the box; −1 and 0, inside it, are in ink.

## Round 2, fresh readers 4 and 5: the page after the changes (2026-11-07)

**What was read.** Commit 5363a54, after the changes above. There were 24 steps, each as a screenshot at 390 px in light with its words, and the page's text step by step with every "Source" opened (`page-text.txt`, taken from the page). The readers were fresh: neither had seen any earlier reading.

**The instructions, as given.** Reader 4's were reader 2's, and reader 5's were reader 3's, word for word: the same persons, the same five questions (six for the layperson), and the same question about the steps not understood. Only the files differed: the 24 new screenshots and the new page text.

### Reader 4 (broad education, no statistics), verbatim

> 1. "The chance my vote matters" means the chance that my one ballot changes who wins. It does not mean "my vote counts" in a feel-good sense. Step 1 shows a race where I'm counted or not and the same side wins either way, so my ballot changed nothing. Steps 2 to 4 show when it does change something. That happens only when everyone else's votes are exactly tied, or my side is one vote behind. In the made-up town of 2,000 voters the page puts this at about 1 in 468. I take that to mean that if you could replay the election 468 times, my ballot would be the deciding one in about one of them (steps 11 and 16). The page says that only this one reason for voting is being weighed. Duty and having a say are set aside (last line of step 24). I'm not sure what "a run of the election" literally is. I guessed it is an imagined replay.
>
> 2. A tie matters because it's the only situation, apart from being one short, where one extra ballot flips the outcome. Otherwise the winner is the same with or without me (step 1). A tie is settled by a coin toss, and the page says my side would win half the time anyway. So when everyone else is tied, my ballot only takes my side from a 50% chance to a sure win. That is half a change. When my side is one behind, my ballot takes it from a sure loss to a coin toss. That is also half a change. So each of the two cases counts as half, and the overall chance is half the chance of "tie or one short" (the half-filled circles in steps 3 and 4, and the half-height blue bar in step 5). I follow this. I'm only partly sure why step 4 says "half + half = one change". It looks as if two halves make a whole, but in any one election only one of the two situations can happen. I think it means "weight each at half", but that is a guess.
>
> 3. For the big race, I think the answer is that with more voters, the chance of any exact count gets thinner. Steps 6 and 7 show the curve flattening almost to a line, with the chance going from 1 in 468 to 1 in 4,558 to 1 in 45,460. The page shows this but never says why in words. The word "tie" had to carry it for me, and I filled in the reason myself. For "lopsided", steps 8 and 9 slide the curve toward 56–44 and 60–40. The 50–50 tie spot ends up far out in the thin edge of the curve, so it's very unlikely (1 in 1,183, then 1 in 7,563). A small, close race has the tie spot near the peak of the curve. Step 10 surprised me. "Less sure" (give or take 8) makes the chance smaller (1 in 836), not bigger. I'd have guessed that being less certain would make a tie more likely. I can see on the picture that the curve got flatter, but I couldn't explain why.
>
> 4. The break-even stakes are the least the result must be worth to me for the trip to the polls to be worth it. The page says it is my cost times N, where my chance is 1 in N. The cost is $8.87 a trip. That comes from 14 minutes at the polls (a typical voter's time, from a 2016 study by Chen, Haggag, Pope and Rohla) at $38 an hour (average US hourly pay, Bureau of Labor Statistics, October 2026, preliminary). N is 468 for the town race, from the site's model. So 468 × $8.87 = about $4,150. If the result is worth $1,000 to me it doesn't pay (step 17), and if it is worth $10,000 it does (step 18). The reasoning I followed is that in 468 replays I make 468 trips but only one of them decides the race, so the result has to be worth more than all those trips together. The page never writes "chance × worth versus cost", so I pieced that together. Also, the "$38 an hour" is an average, not my own pay, even though the page calls it "your cost". And "what the result is worth to you" is left entirely to me, with $1,000 and $10,000 given only as examples.
>
> 5. The presidency chance is tiny for two reasons that I could follow. First, millions of people vote, so an exact tie is extremely unlikely, the same pattern as steps 6 and 7. The 2008 "closest states" figure is 1 in 10 million (step 12). Second, in step 13 my ballot first has to change my state's winner (Pennsylvania, 1 in 1.4 million). Then that state has to be the one that decides the Electoral College, which happens in only 19 in 100 of those runs (step 14). Multiplying those gives about 1 in 7.5 million (step 15). I'm confident of the general idea. I'm less sure why the page gives two different presidency figures, 1 in 10 million and 1 in 7.5 million, without saying how they relate. I also don't know why a "forecast" is used for 2024, since that election is over.
>
> Steps I didn't understand, or understood only partly, and why:
>
> - Step 1: The two dot grids look identical, so the picture shows me nothing. I only got the point from the captions "1,040 to 960" and "1,039 to 960". "Counted / Not counted" isn't explained as "with my ballot / without it". "Stylised" is vague.
> - Steps 3 and 4: The row of circles from -3 to +3 is "your side's lead, not counting you". I had to work out that -1 means my side is one behind, and that the labels apply to both rows although they sit only under the bottom row. Which half of each circle is blue wasn't clear to me. The dashed lines to "= one change" are faint and run across the number labels. See also the "half + half" doubt in answer 2.
> - Step 5: This is where I was most lost on the picture. I didn't know how to read the bell curve. The "give or take" bar had no stated meaning beyond the legend. The axis "how likely" has no numbers. The thin bar's height doesn't feel like "1 in 468". The text explaining that the curve's height is the chance of each exact count appears only in step 6's note, after the picture has already used it.
> - Steps 6 and 7: The dashed "before" curve looks lower than the solid curve I saw in step 5. I couldn't tell whether that was my misreading or a change of scale. In step 7 the marker is a tiny triangle and I couldn't see the bar. The curve shrinking made me wonder whether the election itself was "less likely".
> - Steps 8 to 10: In step 8 the curve looked taller and narrower, not just shifted. I couldn't tell whether the give-or-take had changed, because no new "give or take" figure appears in the step 8 caption (only 2,000 voters and 56–44). Step 10 is counterintuitive, as in answer 3. Also, "1 in 836" is a smaller chance than "1 in 468", and the bigger number being the smaller chance kept tripping me.
> - Step 12: The grid is a grey texture and I can't read individual dots, so I took it as "too many to see". I also don't know which states are the "closest states, 2008".
> - Step 13: The grid is a small speck, and "Pennsylvania, 2024, under the site's model's forecast" confused me.
> - Step 14: This is mostly clear, but "decides the Electoral College" assumes I know how a state can tip it.
> - Step 20: I understood this only partly. It suddenly switches to "what it is worth to everyone" (30 cents each across 300 million people). It isn't clear why my break-even should count other people's gains, or why the seesaw is "level". The black dots are "a million people each", but nothing says that I'm assumed to value everyone's gain equally.
> - Step 21: The number line mixes $8.87, $4,150 and $89 million with labels $1, $1,000, $1 million and $1 billion. The labels are unevenly spaced and the page never says the scale jumps by thousands. So "$1,000 almost touching $1 million" looks wrong. I couldn't tell what the arrow lengths mean. The letter N is also algebra to me.
> - Steps 22 to 24: These are mostly clear. "Shared over 10 million trips" took a moment, and I worked it out as $50 million ÷ 10 million = $5. I also wondered where $50 million, $400,000 and $1,000 come from. The page says they are only examples. I get the final point: the three races together repay $9.36 against an $8.87 trip, so one trip votes in every race and the shares add up.
>
> Overall I understood steps 11 to 19 and 22 to 24 well, steps 1 to 4 once I thought about them, and steps 5 to 10, 12 to 14 and 20 to 21 only partly.

### Reader 5 (total layperson), verbatim

> 1. As far as I can tell, "the chance my vote matters" is the chance that my one ballot is the one that decides who wins. Step 1 shows two pictures of a pretend town race, one with my ballot counted and one without, and the same side wins either way. Most of the time my vote changes nothing. Step 2 shows the rare case. With my ballot it is 1,000 to 1,000 and a coin toss. Without it, it is 999 to 1,000 and the other side wins. The "1 in 468" is that rare case, shown as one ringed dot among 468 (step 11). I took "a run of the election" to mean "imagine the election happening again and again". The page never says that, so I'm guessing. I also can't say how the 468 itself was worked out, so I'm taking it on trust.
>
> 2. A tie matters because that is the only kind of finish where one vote can swing things. If the others are one vote short and I vote, I turn a sure loss into a coin toss. If the others are tied and I vote, I turn a coin toss into a win. A tie is settled by a coin toss, and my side would have won half the time anyway, so my vote only adds half a win in each case. Step 4 says "half + half, one change", and the Source note says the same. I follow that in words. I could not follow the circles in steps 3 and 4 well enough to explain why the two halves add up to one.
>
> 3. I can see what happens but not why. With more voters (steps 6 and 7) the hump gets low and flat, and the number goes from 1 in 468 to 1 in 4,558 to 1 in 45,460. With a lopsided race (steps 8 and 9) the hump slides away from the 50–50 mark, and the number goes to 1 in 1,183 and then 1 in 7,563. The lopsided one makes some sense to me. If one side is far ahead, an exact tie is very unlikely. For more voters I'd only guess that one vote is a smaller drop in a bigger bucket, and the page doesn't say so. Step 10, "less sure", gave 1 in 836, which is a worse chance than before. I would have expected "less sure" to make a tie more likely, not less.
>
> 4. The page never says "break-even stakes". It says "the least the result must be worth to you". As I read it, if my vote matters only once in 468 times, I'd make 468 trips to vote for it to matter once. The cost is $8.87 per trip, so that's 468 × $8.87 = $4,150. The result has to be worth more than $4,150 to me, or it isn't worth going. The $8.87 comes from 14 minutes at the polls, from a study, at $38 an hour, an average pay figure from a government source. I can't check that sum, so I accept it. I wasn't sure whether the $38 is meant to be my pay or just an average. The 468 comes from the page's pretend town race. The rule is "your cost × N", and I guessed N is the number after "1 in".
>
> 5. Millions of people vote, so my one vote is a speck. Step 12 shows a grey mass of tiny dots with one ringed dot lost in it, 1 in 10 million. Steps 13 to 15 add a second hurdle. First, my vote has to change my state's winner (Pennsylvania, 1 in 1.4 million). Second, that state has to be the one that decides the whole country (19 in 100 of those cases). The two together give 1 in 7.5 million. I can't see how the page got from 1.4 million and 19 in 100 to 7.5 million, so I'm trusting it. It also bothered me that step 12 says 1 in 10 million is where a voter's chance was "best", but step 15 gives a better chance, 1 in 7.5 million.
>
> 6. The race changes how many trips it takes before my vote matters once. With the same $10,000 of value to me, the small town race pays and the presidency doesn't (steps 17 to 19). The town needs only $4,150 and the presidency needs $89 million, because it's 10 million trips for one that matters. I got that from the see-saw pictures. At the end (steps 22 to 24) none of the three pays alone. But one trip votes in every race, so the small shares ($5.00, $2.22, $2.14) add up to $9.36. That is more than the $8.87 it costs, so voting pays overall. The "weighing a small chance of a big prize" idea is not something I know, so I'm only repeating the trips story. I don't know how I'd decide what a result is "worth" in dollars. The page says that is up to me.
>
> Steps I didn't understand, or only partly
>
> - Step 3: I couldn't read the row of circles under "your side's lead, not counting you", with numbers from −3 to +3. I don't know what a lead of −1 or 0 means. I also couldn't tell why the "Counted" and "Not counted" rows differ at the two boxed spots. I did understand the half-black, half-grey circle means a coin toss.
> - Step 4: I couldn't tell which circles the dashed lines run from. The blue halves are small, and the key's tiny half-blue mark is hard to tell from the half-black one. I understood "= one change" only from the words.
> - Step 5: I couldn't tell what the horizontal line across the hump measures. I couldn't tell how the filled blue bar becomes "1 in 468". I guessed it is half of the outlined box, because of the "half" idea. I also don't know where 52–48 sits on the bottom line, since only 40%, 50–50 and 60% are marked.
> - Steps 6 and 7: I got the direction but not the reason. In step 7 the bar is invisible, and I only had the number and a tiny triangle.
> - Step 10: I don't know why "less sure" makes the chance worse.
> - Steps 11 and 12: I understood the dots, but "a run of the election" is never explained. In step 12 the dots are too tiny to tell apart.
> - Step 14: "Electoral College" is never explained. I also wasn't sure which "runs" the "19 in 100" refers to. I guessed the arrow means "those where my vote changes my state".
> - Step 15: I couldn't see how the two steps combine into 7.5 million.
> - Step 20: I didn't understand why I should count what the result is worth to everyone, or what "level: they weigh the same" is telling me. The 30¢ and the 300 million dots made no sense to me as a reason.
> - Step 21: The line of $1, $1,000, $1 million and $1 billion is spaced evenly, though each step is far bigger than the last. So $8.87 and $4,150 look close together, which misled me. "N" is a bare letter I had to guess.
> - Steps 22 to 24: The presidency is worth $10,000 in step 19 but $50 million in step 22. I wasn't sure which was meant. I don't know what "the House race" is. The "$5.00 of the $8.87" and "shared over" wording is hard without doing the division. I couldn't do $400,000 ÷ 180,000 or $1,000 ÷ 468 in my head, so I took $2.22 and $2.14 on trust.

### What the second reading found

Both fresh readers answered every question rightly, the layperson's sixth too: the small, sure cost against a tiny chance pays where the chance is less tiny or the result worth more, and one trip pays for the whole ballot. Neither misread "by lot", the sizes of the presidency's fields, the share's dots or the ballot's colours, which were misses of round 1.

What both still understood only partly:

- **Why more voters, or a less sure forecast, lowers the chance.** Both saw that it does, from the curve. Neither could say why, and both expected "less sure" to raise it. The pictures show the effect; the reason (the same chance spread over more counts, or a wider range, stands lower at any one) is in the model note, not on the screen.
- **What a run of the election is.** Both guessed it rightly ("an imagined replay"; "the election happening again and again"). The key now says so: "one run: the same election, held again".
- **Counting what it is worth to everyone (step 20).** Both took the arithmetic, and neither saw why one would count other people's stakes. That is a reason, not a picture; the brief asks for both readings, for you and per person, and the step shows the second as a level seesaw.
- **The scale of dollars (step 21).** Both read its spacing as misleading, as in round 1.
- **The presidency's two figures.** Reader 4 could not tell how 2008's 1 in 10 million and Pennsylvania 2024's 1 in 7.5 million relate; reader 5 was bothered by the source's word "best" (below). Each step names its race and year; the brief asks for both.
- **The Electoral College.** It is now named, but neither reader knew how a state's votes decide it, and reader 5 could not see how 1 in 1.4 million and 19 in 100 make 1 in 7.5 million.
- **The curve's give or take.** Reader 4 read the bracket from its key; reader 5 could not tell what it measures.

One wording error was found and fixed. Reader 5 noted that the source of step 12 called 2008's 1 in 10 million the "best" chance, while step 15 gives Pennsylvania in 2024 a better one, 1 in 7.5 million. The source now says only "The closest states of 2008: about 1 in 10 million". These two word changes, this one and the key's "held again", were made after the second reading and were not read again: the brief asks for one more reading, not a third.
