--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.4
-- Dumped by pg_dump version 9.5.14

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: groups_data; Type: TABLE; Schema: public; Owner: muser
--

CREATE TABLE public.groups_data (
    group_id character varying(50) NOT NULL,
    event_id character varying(50) NOT NULL,
    event_data jsonb,
    rec_update timestamp without time zone DEFAULT now()
);


ALTER TABLE public.groups_data OWNER TO muser;

--
-- Name: groups_list; Type: TABLE; Schema: public; Owner: muser
--

CREATE TABLE public.groups_list (
    group_name character varying(100),
    group_id character varying(50) NOT NULL,
    rec_update timestamp with time zone DEFAULT now()
);


ALTER TABLE public.groups_list OWNER TO muser;

--
-- Name: COLUMN groups_list.group_name; Type: COMMENT; Schema: public; Owner: muser
--

COMMENT ON COLUMN public.groups_list.group_name IS 'Название группы';


--
-- Name: groups_data_pk; Type: CONSTRAINT; Schema: public; Owner: muser
--

ALTER TABLE ONLY public.groups_data
    ADD CONSTRAINT groups_data_pk PRIMARY KEY (group_id, event_id);


--
-- Name: groups_list_pk; Type: CONSTRAINT; Schema: public; Owner: muser
--

ALTER TABLE ONLY public.groups_list
    ADD CONSTRAINT groups_list_pk PRIMARY KEY (group_id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

