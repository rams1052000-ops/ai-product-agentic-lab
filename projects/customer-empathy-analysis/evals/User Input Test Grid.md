# User Input Test Grid
ID	Scenario	Customer input	Expected result
001	Generic negative	App does not work at all.	Negative; broad functionality theme
002	Specific negative	Checkout fails every time I pay.	Negative; checkout failure
003	Mixed	Checkout fails, but search works great.	Mixed; two themes
004	Positive	The app is fast and easy to use.	Positive; speed and usability
005	Neutral	I used the app yesterday.	Neutral; no invented issue
006	Ambiguous	This could be better.	Avoid invented problems
007	Emotional	I hate this app!	Negative; no specific defect invented
008	Critical	All my saved data disappeared.	Potential critical data loss
009	Multiple issues	Login is slow and checkout crashes.	Two negative themes
010	Explicit vs. inferred	I waited 10 minutes for the page to load.	Explicit slowness; don't invent a cause
011	Empty input	(blank)	Validation error
012	Duplicate	Submit the same source ID twice	Duplicate excluded from official counts