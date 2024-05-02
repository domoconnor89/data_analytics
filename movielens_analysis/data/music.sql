/* to execute this file:

psql -U postgres -p 5432 -h 34.141.104.250 -d music -f music.sql
*/


-- create the table 'bands'

drop table if exists bands;
create table bands(
    band_name VARCHAR(255) primary key,
    style VARCHAR(255),
    members INT);

-- impute the data from a csv into the table

INSERT INTO bands (band_name, style, members) VALUES ('Madness', 'two-tone', 7);
INSERT INTO bands (band_name, style, members) VALUES ('The Cars', 'new wave', 5);
INSERT INTO bands (band_name, style, members) VALUES ('The Runaways', 'punk', 4);
INSERT INTO bands (band_name, style, members) VALUES ('Blondie', 'punk', 5);
INSERT INTO bands (band_name, style, members) VALUES ('Talking Heads', 'new wave', 4);
INSERT INTO bands (band_name, style, members) VALUES ('Joe Jackson', 'jazz', 5);
INSERT INTO bands (band_name, style, members) VALUES ('Weather Report', 'fusion-jazz', 4);

-- create the table 'songs'
DROP table if exists songs;
create table songs(
    band_name VARCHAR(255),
    song VARCHAR(255) primary key);

-- impute the data from a csv into the table
\COPY songs FROM './songs.csv' DELIMITER ',' CSV HEADER;


/* Adding a Foreign Key

The syntax for adding a PK using ALTER TABLE:
ALTER TABLE child_table_name
ADD FOREIGN KEY (child_foreign_key_column_name) REFERENCES parent_table(parent_primary_key_column);
 */

ALTER TABLE songs
ADD FOREIGN KEY (band_name) REFERENCES bands(band_name);

/* 
Cascade

One of the main reasons that tables are connected using primary and
foreign keys is to ensure the integerity of the data. These relationships 
prevent the deletion or alteration of data one table that has a parent-child 
relationship with another.

The parent-child relationship prevents the parent table from being dropped using a normal DROP TABLE command.

For example, normal drop will not work now in the below:        */

DELETE FROM bands WHERE band_name = 'Blondie';
/* this gives the following ERROR MESSAGE... having added the foreign key, delete request is blocked:
-----------------------------------------------------------------------------------------------------
SQL Error [23503]: ERROR: update or delete on table "bands" violates foreign key constraint "songs_band_name_fkey" on table "songs"
  Detail: Key (band_name)=(Blondie) is still referenced from table "songs".
-----------------------------------------------------------------------------------------------------

The work around is adding the CASCADE argument.
This will in turn not only drop the parent table but will cascade to all the children tables... 
... and drop the foreign key contraints.

!!! NOW SWITCH TO THE 'music.sql' FILE IN '07_foreign_keys' FOLDER !!!

*/
