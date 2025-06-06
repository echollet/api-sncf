CREATE TABLE types_enum (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, typename TEXT NOT NULL);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE stop_points (id TEXT PRIMARY KEY NOT NULL, name TEXT NOT NULL, label TEXT NOT NULL, id_type INTEGER REFERENCES types_enum (id));
CREATE TABLE stop_areas (id TEXT PRIMARY KEY NOT NULL, name TEXT NOT NULL, label TEXT NOT NULL);
CREATE TABLE lines (id TEXT PRIMARY KEY NOT NULL, name TEXT NOT NULL, code TEXT NOT NULL, network TEXT REFERENCES networks(id));
CREATE TABLE lnk_line_route (line_id TEXT REFERENCES lines (id), route_id TEXT REFERENCES routes (id));
CREATE TABLE lnk_stop_point_line (stop_point_id TEXT REFERENCES stop_points(id), line_id TEXT REFERENCES lines (id));
CREATE TABLE routes (id TEXT PRIMARY KEY NOT NULL, name TEXT NOT NULL, code TEXT, line TEXT);
CREATE TABLE networks (id TEXT PRIMARY KEY NOT NULL, name TEXT NOT NULL);