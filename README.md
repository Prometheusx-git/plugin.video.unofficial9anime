
# UP9anime, aka The Unofficial Plugin for 9anime
An unofficial 9anime client for Kodi version 16 and up, designed for the Fire Stick, Fire TV, and Windows.
This is a fork of the UP9anime addon originally created by dat1guy.

 - [Installation](#installation)
 - [Features](#features)
 - [Known Issues](#known-issues)

## Installation
Download the repo from [here](https://github.com/Prometheusx-git/repository.unofficial9anime/master/repository.unofficial9anime).  DO NOT install the add-on using the green button above, as this add-on requires dependencies only found in the repository.

Once the repository is installed to Kodi, install the add-on from the repository from within Kodi.

## Features
### Enhanced metadata support
As mentioned previously, the built-in metahandlers plugin has been extended and modified to work better with anime shows and Japanese media.  There are still some gaps or peculiarities, but my hope is that the support is better than other plugins for similar content.

Furthermore, users can fix or find metadata for shows with incorrect or absent metadata.  The process includes suggestions populated from aliases of the show from the 9anime website, which often will do the trick!

Note that metadata is stored by the metahandlers plugin in a database shared by dat1guy's add-ons like UP9anime and UKAP, instead of in the metahandlers database, because the database structure has been modified.

### Browse
Users can browse the plugin in a similar fashion to the 9anime website, which includes categories like Most Watched, Upcoming, Genres, and Trending.

### Search
Users can search for shows in the plugin.

### Account watch list
Users can log in to their accounts and browse and modify their watch list, including individual folders.  Users can also preset the folder to view in the settings.

### Last show visited
Users can see the last show they visited from the main menu, for quick access for continuing a series.

### Quality selection
The default quality of the video can be preset in the settings or individually selected for each piece of media.

### Sorting
The default ordering of shows when browsing can be preset in the settings or individually selected.

### Queueing
Users can queue episodes or movies into a playlist and then play the playlist without interruption.  If the user disables related links in the settings, users can also quickly queue entire TV shows.

### Widget support
Widgets in supported skins can be populated with any page of the plugin (except search), including the bookmarks and the last show visited.

## Known Issues
 - Metadata for movies is pretty lackluster by default. Users can get better results by inputting a [TMDB API key](https://www.themoviedb.org/faq/api?language=en) in the settings.
 - Metadata support for specials and OVAs is lackluster.
 - Queueing a show when related links are enabled results in an infinite loop.  This cannot be fixed, but a workaround is available by disabling related links in the settings.

