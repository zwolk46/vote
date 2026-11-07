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
