# KnowledgeBase
A simple Database for Ros

## Dependencies
- python
  - pymongo 
  - mongoengine
- distibution
  - mongodb

This repository has a corresponding message file repository: https://github.com/Slothologist/KnowledgeBase_mgs

## Overview

### Starting the rosnode
Use the launchfile contained in the launch folder. A config file for the KBasenode must be
given as additional paramenter. You will find one in the useful_files folder.

### Physical location of the database
MongoDB's default saving location is under /var/lib/mongodb. This can be changed in the
/etc/mongod.conf or by starting a mongo daemon with the --dbpath or --config parameters.

### Pipeline for creating a new KnowledgeBase

1. create a new annotation file (with the clf map annotation tool)
1. edit the generate_example_data.py file to fit your needs (objects, location & rooms, persons, etc.)
1. parse this annotation file to the new btl format using the map_annotation_tool_to_btl_converter.py
1. start a mongo deamon where the dbpath is the directory in which you want to save your databases (and the port matches the port specified in generate_example_data.py)
   1. Caution: Mongodb creates journal files by default which are quite big, used for storing history. You may not want to copy them.
1. use the generate_example_data.py script to write into mongodb
1. terminate the mongo deamon and push your changes

Alternatively you can execute step one and two, then use the generate_and_upload.py in the 
useful_files directory to automate the rest of the steps.

## Database Schema
coming soon...

## Services
The Node realises queries as Ros Servicecalls. The main call for queries is under the topic 
/KBase/query, accepts a query in string form and returns one or more database objects in xml 
form. The secondary call is found under /KBase/data, accepts a command and return a success 
boolean and an error code.

## Queries

Queries are accepted in a form inspired by native human speech. Each query starts with a question
word, e.g. where, who, what, which, when. This word defines the type of the return value.

Queries can be enhanced by adding 'filler' words, making the queries more human-like. These 
filler words are (amongst others) 'are', 'is', 'was', 'the', 'of', 'that', 'were', 'have' and 'has'.
This makes theses queries valid:
* where is the kitchen
* what is the size of the milk
* which rcobjects have the shape cylindrical
* in which room is the cup
* how many category have the rcobjects


### Where
Will return a Viewpoint corresponding to a given identifier. 'Where' queries shall be of the form 
'where *unique_identifier* [*viewpoint_label*]'. The *unique identifier* can be of either a 
Location, Person, Room or RCObject. The optional *viewpoint label* can be specified to retrieve a 
specific viewpoint a Room or Location may have by its label. If *viewpoint label* is not specified,
the Viewpoint with label 'main' will be used. 

##### Examples
* where kitchen
  * Will return the main viewpoint of the room 'kitchen'
* where fridge grasp_loc_1
  * Will return the viewpoint with label 'grasp_loc_1' of the location 'fridge'
* where michael
  * Will return the 'position' of the person 'michael'
* where cup
  * Will return the viewpoint with label 'main' of the object 'cup'


### What
Will return a RCObject (or String). 'What' queries shall be of the form 'what [*attribute_name*]
*unique_identifier*'. The *unique identifier* shall be the 'name' of a RCObject. The optional 
*attribute name* can be specified to retrieve (instead of the complete RCObject) the value of a
specific attribute of the RCObject specified by the *unique identifier* as a String.

##### Examples
* what cup
  * Will return the RCObject with name 'cup'
* what shape melon
  * Will return a string which is the 'shape' of the RCObject with name 'melon'
* what color apple
  * Will return a string which is the 'color' of the RCObject with name 'apple'

### Which
Will return a List of basic database objects (BDO, i.e. Person, Location, Room, Door, RCObject)
where a given attribute has a given value. 'Which' queries shall be of the form 'which *BDO* 
*attribute* *value*'. The *BDO* must be either 'Location', 'Person', 'Room' or 'RCObject'. The 
*attribute* must be one of the attributes the *BDO* has. The *value* shall be the value of the
given *attribute*.

##### Examples
* which rcobject color green
  * Will return a List of RCObject. Every 'color' of these RCObject will have the value 'green'
* which room name kitchen
  * Will return a List of Room. Every Room's 'name' attribute will have the value 'kitchen'. Note 
  that this List will probably have length 1.
* which person gender female
  * Will return a List of Person. Every Persons 'gender' attribute will have the value 'female'.

### Who
will return a Person or List of Persons corresponding to a given identifier. 'Who' queries shall 
be of the form 'who *unique_identifier*. The *unique identifier* shall be the 'name' or 'uuid' of
a Person. 

##### Examples
* who peter
  * Will return the Person with the 'name' attributes value being 'peter' 
 
### In which
Will return either a Location or a Room. 'In which' queries shall be of the form 'in which
('Location' | 'Room') *unique_identifier*'. The *unique identifier* can be of either a 
Location, Person, Room or RCObject. The second argument so to say must be either 'Location' or 
'Room' and will determine, if this query returns a Location or Room.

##### Examples
* in which room cup
  * Will return the Room in which the Location lies, in which again the RCObject with the 'name'
   attribute 'cup' is located.  
* in which location alex
  * Will return the Location in which the 'position' of the Person with the name 'alex' 
  is located. Note that this may return just a String with a error message, if alex is not known 
  to be in any Location.
* in which room point *<Point2D_xml>*

### How many
Will return a int corresponding to the number of distinct occurences a specified attribute has
in a BDO. 'How many' queries shall be of the form 'how many *attribute* *BDO*'. The 
*BDO* must be either 'Location', 'Person', 'Room' or 'RCObject'. The 
*attribute* must be one of the attributes the *BDO* has.

##### Examples
* how many category rcobject
  * Will return an Int which is equal to the number of distinct attribute 'category' values of all 
  the known RCObject instances have. 
* how many name person
  * Will return an Int which is equal to the number of distinct attribute 'name' values of all the 
  known Person instances have. Because in this case 'name' is the unique identifier, this querry 
  will return the number of distinct Persons.

### Get
With get you can retrieve a non basic data object. 'Get' queries shall be of the form 'get *NBDO*'.
The *NBDO* must be either 'KBase', 'Arena', 'Context', 'RCObjects' or 'Crowd'.

##### Examples
* get kbase
  * Will return the entire Knowledgebase as an KBase object.
* get ARENA
  * Will return the entire Arena, with all Locations, Rooms and Doors as Arena object.

## Saving or deleting Data 
Thee are realised by the /KBase/data rosservice call. Each command given over it starts with a 
command word, i.e. remember or forget. As well as the queries of the query call the commands are 
designed to somehow resemble human speech. As objects are transmitted via xml, this is somewhat 
lackluster, especially for remember. 

Commands can also be enhanced with filler words, see above.

### Remember
Will save a BDO in the KBase. 'Remember' commands shall be of the form 'remember *BDO*'. The 
*BDO* must be either a Location, Person, Room or Rcobject in XML-form. To see how the BDOs shall
be represented, take a look at the *_cleaned.xml in the useful files folder or uncomment the lines 
at the end of the generate_example_data.py to print a complete KBase in xml format. (Note: The 
Generator and Timestamp elements are optional and required for downwards compatibility)

##### Examples
```
remember <ROOM name="kitchen" numberofdoors="2">
            <ANNOTATION label="room:kitchen">
                <VIEWPOINT label="main">
                    <POSITIONDATA frameid="map" theta="0.179018005729">
                        <POINT2D x="14.376999855" y="5.93919992447"/>
                    </POSITIONDATA>
                </VIEWPOINT>
                <PRECISEPOLYGON>
                    <POINT2D x="14.1516796875" y="7.02464013672"/>
                    <POINT2D x="16.1996806641" y="6.63552001953"/>
                    <POINT2D x="16.0972802734" y="5.36575976562"/>
                    <POINT2D x="14.0492802734" y="5.632"/>
                </PRECISEPOLYGON>
            </ANNOTATION>
         </ROOM>
```
Will save a annotation as defined above.

```
remember <PERSONDATA name="michael" uuid="12345678" faceid="87654321"
              gender="male" shirtcolor="green" posture="standing"
              gesture="waving" age="20-25">
              <POSITIONDATA frameid="map" theta="0.179018005729">
                 <POINT2D x="14.376999855" y="5.93919992447"/>
              </POSITIONDATA>
         </PERSONDATA>
```
Will save a Person named michael as defined above.

### Forget
Will delete a BDO from the KBase. 'Forget' commands shall be of the form 'forget 
*unique_identifier*'. The *unique identifier* can be of either a Location, Person, Room or 
RCObject. Another form, added for convieniance is 'forget all *BDO*'. The *BDO* 
must be either 'Location', 'Person', 'Room', 'Door' or 'RCObject' (Plurals are allowed as well).
It deletes every BDO of the given type.

##### Examples
* forget michael
  * Will delete the Person with name Michael from the database
* forget all the locations
  * will delete all Locations from the database

## Error Codes
Error codes are valid if and only if the success field in the Service answers is false.

### Query

#### 0
The question word was not in the list of accepted or supported question words.

#### Starting with 1: What queries
 - 11
   - There is no Object with the specified name.
 - 12
   - There is a BDO with the specified name but it is no Object.
 - 13
   - The type of the requested variable of the object is not xml-ifieable and could thus not send back.

#### Starting with 2: Where queries
 - 21
   - The name of the BDO provided by the query could not be found.

#### Starting with 3: In which queries
 - 31
   - The name of the BDO provided by the query could not be found.
 - 32
   - You asked in which Location a specific Room lies, which makes no real sense. In the Knowledgebases world, rooms do not lie in locations but the other way round.
 - 33
   - Something unforseen happened. Maybe the BDO/ Point specified by the query does not lie in any room/ location.

#### Starting with 4: Which queries
 - 41
   - The name of the class of BDO is not viable.

#### Starting with 5: How many queries
 - 51
   - The name of the class of BDO is not viable.
   
#### Starting with 6: Who queries
 - 61
   - There is no Person with the specified name or uuid.
 - 62
   - There is a BDO with the specified name but it is no Person.

#### Starting with 7: Get queries
 - 71
   - The name of the requested Class is not viable.

### Data

#### 0
The data storage word was not in the list of accepted or supported data storage words.

#### Starting with 1: Forget queries
 - 81
   - Command was ill formatted. There was more than tree elements and the second one was not 'all'
 - 82
   - The specified class of which all objects should be deleted is not allowed or supported.
 - 83
   - There was no BDO with the specified identifier to be deleted.
   
#### Starting with 2: Remember queries
 - 91
   - The given XML could not be parsed (aka was no valid xml)
 - 92
   - The given XMLs basetag is not available for converting to a BDO
 - 93
   - The given XML failed to be converted to a BDO
 - 94
   - The BDO specified a Location that could not be found
 - 95
   - The BDO specified a Room that could not be found

## Todos
* Test data retrieval after deleting
  * NBDOs seem to have a problem with their references if they get deleted
* add missing from_xml functions
  * room, annotation, door, location, rcobject