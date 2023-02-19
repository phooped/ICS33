# p2app/engine/main.py
#
# ICS 33 Winter 2023
# Project 2: Learning to Fly
#
# An object that represents the engine of the application.
#
# This is the outermost layer of the part of the program that you'll need to build,
# which means that YOU WILL DEFINITELY NEED TO MAKE CHANGES TO THIS FILE.
import sys

from p2app.events import *


import sqlite3


class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        self._conn = None
        self._cursor = None


    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""

        # Database
        if isinstance(event, OpenDatabaseEvent):
            try:
                self._conn = sqlite3.connect(event.path())
                self._cursor = self._conn.cursor()
                self._cursor.execute('select * from sqlite_master')
                self._cursor.execute('PRAGMA foreign_keys = ON;')
                yield DatabaseOpenedEvent(event.path())
            except Exception as e:
                yield DatabaseOpenFailedEvent(str(e))

        if isinstance(event, QuitInitiatedEvent):
            self._conn.close()
            yield EndApplicationEvent()
            sys.exit()

        if isinstance(event, CloseDatabaseEvent):
            self._conn.close()
            yield DatabaseClosedEvent()


        # Continent
        if isinstance(event, SaveNewContinentEvent):
            try:
                if not event.continent()[1] or not event.continent()[2]:
                    raise Exception('Code or name cannot be empty')

                #Check if continent code is unique
                self._cursor.execute('select exists (select 2 from continent where continent_code = (:continent_code))',
                                     {'continent_code':event.continent()[1]})
                if self._cursor.fetchone()[0]:
                    raise Exception('Continent code already in use')

                query = 'select max(continent_id) from continent'
                self._cursor.execute(query)

                result = int(self._cursor.fetchone()[0])
                newContinentID = result + 1

                self._cursor.execute('INSERT INTO continent (continent_id,continent_code,name) values (:newContinentID,:continentCode,:name);',
                                     {'newContinentID':newContinentID,'continentCode':event.continent()[1],'name':event.continent()[2]})
                self._conn.commit()

                yield ContinentSavedEvent(event.continent())
            except Exception as e:
                yield SaveContinentFailedEvent(str(e))


        if isinstance(event, StartContinentSearchEvent):
            if event.name() == None and event.continent_code() == None:  # Both empty
                pass
            elif event.continent_code() == None: #Continent code empty
                self._cursor.execute('select continent_id,continent_code,name from continent where name = (:name)',
                                     {'name':event.name()})
            elif event.name() == None: #Name empty
                self._cursor.execute('select continent_id,continent_code,name from continent where continent_code = (:continent_code)',
                                     {'continent_code':event.continent_code()})
            else: #Both not empty
                self._cursor.execute('select continent_id,continent_code,name from continent where continent_code = (:continent_code) and name = (:name)',
                                     {'continent_code':event.continent_code(),'name':event.name()})

            result = self._cursor.fetchall()

            if len(result)!=0:
                for k in result:
                    yield ContinentSearchResultEvent(Continent(k[0],k[1],k[2]))


        if isinstance(event,LoadContinentEvent):
            self._cursor.execute('select continent_id,continent_code,name from continent where continent_id = (:continent_id)',
                                 {'continent_id':event.continent_id()})

            result = self._cursor.fetchall()

            for k in result:
                yield ContinentLoadedEvent(Continent(k[0],k[1],k[2])) #Takes in Continent


        if isinstance(event, SaveContinentEvent):
            try:
                if not event.continent()[1] or not event.continent()[2]:
                    raise Exception('Code or name cannot be empty')

                #Check if continent code is unique in the case that user changes it
                self._cursor.execute('select continent_code from continent where continent_id = (:continent_id)',
                                     {'continent_id':event.continent()[0]})
                oldContinentID = self._cursor.fetchone()[0]

                if event.continent()[1] != oldContinentID:

                    self._cursor.execute('select exists (select 2 from continent where continent_code = (:continent_code))',
                                         {'continent_coe':event.continent()[1]})
                    if self._cursor.fetchone()[0]:
                        raise Exception('Continent code already in use')


                self._cursor.execute('update continent set continent_code = (:continent_code), name = (:name) where continent_id = (:continent_id)',
                                     {'continent_code':event.continent()[1],'name':event.continent()[2],'continent_id':event.continent()[0]})
                self._conn.commit()

                yield ContinentSavedEvent(event.continent())

            except Exception as e:
                yield SaveContinentFailedEvent(str(e))




        #Country
        if isinstance(event,SaveNewCountryEvent):
            try:
                if not event.country()[1] or not event.country()[2] or not event.country()[3] or not event.country()[4]:
                    raise Exception('Country code, name, continent id, or wikipedia link can\'t be empty')

                #Checks if country code unique
                self._cursor.execute('select exists (select 2 from country where country_code = (:country_code))',
                                     {'country_code':event.country()[1]})
                if self._cursor.fetchone()[0]:
                    raise Exception('Country code already in use')


                query = 'select max(country_id) from country'
                self._cursor.execute(query)

                result = int(self._cursor.fetchone()[0])
                newCountryID = result + 1


                self._cursor.execute('insert into country (country_id, country_code,name,continent_id,wikipedia_link,keywords) values (:country_id,:country_code,:name,:continent_id,:wikipedia_link,:keywords)',
                                     {'country_id':newCountryID,'country_code':event.country()[1],'name':event.country()[2],'continent_id':event.country()[3],'wikipedia_link':event.country()[4],'keywords':event.country()[5]})
                self._conn.commit()

                yield CountrySavedEvent(event.country())
            except Exception as e:
                if str(e) == 'FOREIGN KEY constraint failed':
                    yield SaveCountryFailedEvent('Continent ID entered doesn\'t exist\nPlease enter a valid continent ID')
                else:
                    yield SaveCountryFailedEvent(str(e))


        if isinstance(event, StartCountrySearchEvent):
            if event.name() == None and event.country_code() == None:  # Both empty
                pass
            elif event.country_code() == None:  # Country code empty
                self._cursor.execute('select country_id,country_code,name,continent_id,wikipedia_link,keywords from country where name = (:name)',
                                     {'name':event.name()})
            elif event.name() == None:  # Name empty
                self._cursor.execute('select country_id,country_code,name,continent_id,wikipedia_link,keywords from country where country_code = (:country_code)',
                                     {'country_code': event.country_code()})
            else:  # Both not empty
                self._cursor.execute('select country_id,country_code,name,continent_id,wikipedia_link,keywords from country where country_code = (:country_code) and name = (:name)',
                                     {'country_code':event.country_code(),'name': event.name()})

            result = self._cursor.fetchall()

            if len(result) != 0:
                for k in result:
                    yield CountrySearchResultEvent(Country(k[0], k[1], k[2],k[3],k[4],k[5]))

        if isinstance(event,LoadCountryEvent):
            self._cursor.execute('select country_id,country_code,name,continent_id,wikipedia_link,keywords from country where country_id = (:country_id)',
                                 {'country_id':event.country_id()})
            result = self._cursor.fetchall()

            for k in result:
                yield CountryLoadedEvent(Country(k[0],k[1],k[2],k[3],k[4],k[5]))


        if isinstance(event,SaveCountryEvent):
            try:
                if not event.country()[1] or not event.country()[2] or not event.country()[3] or not event.country()[4]:
                    raise Exception('Country code, name, continent id, or wikipedia link can\'t be empty')

                self._cursor.execute('select country_code from country where country_id = (:country_id)',
                                     {'country_id':event.country()[0]})
                oldCountryCode = self._cursor.fetchone()[0]

                # Checks if country code unique if user wants to change the country code
                if event.country()[1] != oldCountryCode:
                    self._cursor.execute('select exists (select 2 from country where country_code = (:country_code))',
                                         {'country_code':event.country()[1]})
                    if self._cursor.fetchone()[0]:
                        raise Exception('Country code already in use')


                self._cursor.execute('update country set country_code = (:country_code), name = (:name),continent_id = (:continent_id),wikipedia_link = (:wikipedia_link), keywords = (:keywords) where country_id = (:country_id)',
                                     {'country_code':event.country()[1],'name':event.country()[2],'continent_id':event.country()[3],'wikipedia_link':event.country()[4],'keywords':event.country()[5],'country_id':event.country()[0]})
                self._conn.commit()

                yield CountrySavedEvent(event.country())

            except Exception as e:
                if str(e) == 'FOREIGN KEY constraint failed':
                    yield SaveCountryFailedEvent(
                        'Continent ID entered doesn\'t exist\nPlease enter a valid continent ID')
                else:
                    yield SaveCountryFailedEvent(str(e))





        #Region
        if isinstance(event,SaveNewRegionEvent):
            try:
                #Run empty checks
                if not event.region()[1] or not event.region()[2] or not event.region()[3] or not event.region()[4] or not event.region()[5]:
                    raise Exception('Region code, local code, name, continent id, or country id cannot be empty')

                #Check if region code not unique
                self._cursor.execute('select exists (select 2 from region where region_code = (:region_code))',
                                     {'region_code':event.region()[1]})
                if self._cursor.fetchone()[0]:
                    raise Exception('Region code already in use')

                #Retrieve new region_id
                query2 = 'select max(region_id) from region'
                self._cursor.execute(query2)

                result = int(self._cursor.fetchone()[0])
                newRegionID = result + 1

                #Add new row
                self._cursor.execute('insert into region (region_id, region_code,local_code,name,continent_id,country_id,wikipedia_link,keywords) values ((:newRegionID),(:region_code),(:local_code),(:name),(:continent_id),(:country_id),(:wikipedia_link),(:keywords))',
                                     {'newRegionID':newRegionID,'region_code':event.region()[1],'local_code':event.region()[2],'name':event.region()[3],'continent_id':event.region()[4],'country_id':event.region()[5],'wikipedia_link':event.region()[6],'keywords':event.region()[7]})
                self._conn.commit()

                yield RegionSavedEvent(event.region())
            except Exception as e:
                if str(e) == 'FOREIGN KEY constraint failed':
                    yield SaveRegionFailedEvent('Continent ID or Country ID entered doesn\'t exist\n')
                else:
                    yield SaveRegionFailedEvent(str(e))

        if isinstance(event,StartRegionSearchEvent):
            event.region_code(), event.name(), event.local_code()

            if not event.region_code() and not event.name() and not event.local_code():  #All empty
                pass
            elif event.region_code():  # Region code not empty
                self._cursor.execute('select region_id,region_code,local_code,name,continent_id,country_id,wikipedia_link,keywords from region where region_code = (:region_code)',
                                     {'region_code':event.region_code()})
            elif not event.name():  # Name empty
                self._cursor.execute('select region_id,region_code,local_code,name,continent_id,country_id,wikipedia_link,keywords from region where local_code = (:local_code)',
                                     {'local_code':event.local_code()})
            elif not event.local_code():  # local code empty
                self._cursor.execute('select region_id,region_code,local_code,name,continent_id,country_id,wikipedia_link,keywords from region where name = (:name)',
                                     {'name':event.name()})
            else:
                self._cursor.execute('select region_id,region_code,local_code,name,continent_id,country_id,wikipedia_link,keywords from region where name = (:name) and local_code = (:local_code)',
                                     {'name':event.name(),'local_code':event.local_code()})

            result = self._cursor.fetchall()

            if len(result) != 0:
                for k in result:
                    yield RegionSearchResultEvent(Region(k[0],k[1],k[2],k[3],k[4],k[5],k[6],k[7]))

        if isinstance(event, LoadRegionEvent):
            self._cursor.execute('select region_id,region_code,local_code,name,continent_id,country_id,wikipedia_link,keywords from region where region_id = (:region_id)',
                                 {'region_id':event.region_id()})

            result = self._cursor.fetchall()

            for k in result:
                yield RegionLoadedEvent(Region(k[0],k[1],k[2],k[3],k[4],k[5],k[6],k[7]))


        if isinstance(event, SaveRegionEvent):
            try:
                # Run empty checks
                if not event.region()[1] or not event.region()[2] or not event.region()[3] or not event.region()[4] or not event.region()[5]:
                    raise Exception('Region code, local code, name, continent id, or country id cannot be empty')

                #do a unique check in the case that user CHANGES region code
                self._cursor.execute('select region_code from region where region_id = (:region_id)',
                                     {'region_id':event.region()[0]})
                oldRegionCode = self._cursor.fetchone()[0]

                if event.region()[1] != oldRegionCode:
                    self._cursor.execute('select exists (select 2 from region where region_code = (:region_code))',
                                        {'region_code':event.region()[1]})
                    if self._cursor.fetchone()[0]:
                        raise Exception('Region code already in use')

                #Update new row
                self._cursor.execute('update region set region_code = (:region_code), local_code = (:local_code),name =(:name),continent_id = (:continent_id),country_id = (:country_id),wikipedia_link = (:wikipedia_link),keywords = (:keywords) where region_id = (:region_id)',
                                     {'region_code':event.region()[1],'local_code':event.region()[2],'name':event.region()[3],'continent_id':event.region()[4],'country_id':event.region()[5],'wikipedia_link':event.region()[6],'keywords':event.region()[7],'region_id':event.region()[0]})
                self._conn.commit()

                yield RegionSavedEvent(event.region())

            except Exception as e:
                if str(e) == 'FOREIGN KEY constraint failed':
                    yield SaveRegionFailedEvent('Continent ID or Country ID entered doesn\'t exist\n')
                else:
                    yield SaveRegionFailedEvent(str(e))