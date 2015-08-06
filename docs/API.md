API
---

The API requires authentication for most tasks. The ones that do not are marked by a *. 

Authentication is simple - user tokens. Tokens are found in cookies on the desktop-side, and via the QR code login system on mobile. (QR code format is userid:token).

The QR login system allows for mobile users to log in without complex work to allow the server to know they've authenticated to CAS.

You can prove that you have the authorization to use the API by including two variables in POST or GET requests: userid and token. For example: `ssvps.magmastone.net/getPath?node1=nd1&node2=nd2&userid=aj3roth&token=blabla`


The main API endpoint is ssvps.magmastone.net/ . All calls are relative to this. This URL will remain, though our user-facing domain will change.


`/getpath` * GET
---

GetPath is used to get the fastest path between any two nodes.

**Parameters:**

- node1  *(required)* The first node ID.
- node2 *(required)* The second node ID.

**Returns** 

Returns a JSON dict in the form:

`{"path":[{"id":"b-e2","lat"10.20,"lon":-10.231,"name":"hi"}]}`

Expect more keys to be added in the future.


`/getschedule` GET
---

GetSchedule is used to get the day's schedule. All classes for the day are returned.

**Parameters:**
- Standard auth

**Returns**

JSON array in the form

`[{"id":10,"class_name": "SE 101 - Introduction to Software Eng","section":"001","timestamp":"14:50 09/14/2015","timeend":"15:20 09/14/2015","instructor": "Staff","type":"SEM","where":"EIT 1015"}]`

Expect multiple dictionaries, one for each class.

- ID is the unique ID from the schedule table. Can safely be ignored.
- class_name is the full name of the class, including course code.
- section is class section. Does not need to be displayed to user.
- timestamp is start time of the class. Always in 24 hour format like: HH:mm MM/dd/yyyy
- timeend is end time of the class. Identical format
- instructor is the prof teaching the particular class.
- type is the type of course. So far: LAB,LEC,TUT,SEM. Possibly more.
- where is the full building name, including room number. (safe bet is to split at first space to find building ID.)

`/getnextclass` GET
---

GetSchedule is used to get user's next class.

**Parameters:**
- Standard auth

**Returns**

JSON dict in the form

`{"id":10,"class_name": "SE 101 - Introduction to Software Eng","section":"001","timestamp":"14:50 09/14/2015","timeend":"15:20 09/14/2015","instructor": "Staff","type":"SEM","where":"EIT 1015"}`


- ID is the unique ID from the schedule table. Can safely be ignored.
- class_name is the full name of the class, including course code.
- section is class section. Does not need to be displayed to user.
- timestamp is start time of the class. Always in 24 hour format like: HH:mm MM/dd/yyyy
- timeend is end time of the class. Identical format
- instructor is the prof teaching the particular class.
- type is the type of course. So far: LAB,LEC,TUT,SEM. Possibly more.
- where is the full building name, including room number. (safe bet is to split at first space to find building ID.)


`/getclosestnode` * GET
---

GetClosestNode will return the closest nodeID to the user. Used for navigation/location.


**Parameters:**
- lat User's latitude
- lon User's longitude

**Returns**

JSON dict: - probably doesn't need to be, but keeping it consistant.

`{"id":"b-e2","lat"10.20,"lon":-10.231,"name":"hi"}`


`/BuildingList` * GET
---
BuildingList returns a list of all the buildings, along with ID and name.

**Parameters:**
- None!

**Returns**

JSON array:

`[{"name":"Engineering 3", "id":"E3"}]`

**Note that that any building ID can be turned into a node ID by prepending b-**

Example: E3 becomes b-E3.

