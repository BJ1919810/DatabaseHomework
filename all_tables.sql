--
-- openGauss database dump
--

SET statement_timeout = 0;
SET xmloption = content;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET session_replication_role = replica;
SET client_min_messages = warning;
SET enable_dump_trigger_definer = on;

--
-- Name: BEHAVIORCOMPAT; Type: BEHAVIORCOMPAT; Schema: -; Owner: 
--

SET behavior_compat_options = '';


--
-- Name: LENGTHSEMANTICS; Type: LENGTHSEMANTICS; Schema: -; Owner: 
--

SET nls_length_semantics = 'byte';


SET search_path = public;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: admin_login_k; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE admin_login_k (
    admin_id character(20) NOT NULL,
    admin_pass character(20)
)
WITH (orientation=row, compression=no);


ALTER TABLE public.admin_login_k OWNER TO dbuser;

--
-- Name: book_k; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE book_k (
    bookid character(20) NOT NULL,
    title character(20),
    author character(20),
    publisher character(20),
    isbn character(13),
    totalcopies integer,
    availablecopies integer
)
WITH (orientation=row, compression=no);


ALTER TABLE public.book_k OWNER TO dbuser;

--
-- Name: record_k; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE record_k (
    recordid character(20) NOT NULL,
    userid character(20) NOT NULL,
    bookid character(5) NOT NULL,
    borrowdate timestamp(0) without time zone,
    returndate timestamp(0) without time zone,
    duedate timestamp(0) without time zone NOT NULL
)
WITH (orientation=row, compression=no);


ALTER TABLE public.record_k OWNER TO dbuser;

--
-- Name: user_k; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE user_k (
    userid character(20) NOT NULL,
    username character(20)
)
WITH (orientation=row, compression=no);


ALTER TABLE public.user_k OWNER TO dbuser;

--
-- Name: user_login_k; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE user_login_k (
    user_id character(20) NOT NULL,
    user_pass character(20)
)
WITH (orientation=row, compression=no);


ALTER TABLE public.user_login_k OWNER TO dbuser;

--
-- Data for Name: admin_login_k; Type: TABLE DATA; Schema: public; Owner: dbuser
--

COPY public.admin_login_k (admin_id, admin_pass) FROM stdin;
zbj                 	123456              
\.
;

--
-- Data for Name: book_k; Type: TABLE DATA; Schema: public; Owner: dbuser
--

COPY public.book_k (bookid, title, author, publisher, isbn, totalcopies, availablecopies) FROM stdin;
B114                	下北泽银梦     	田所浩二        	下北泽出版社  	1145141919810	100	5
B001                	三体              	刘慈欣           	重庆出版社     	9787536692930	150	50
B002                	test                	somebody            	China               	88888888     	100	1
\.
;

--
-- Data for Name: record_k; Type: TABLE DATA; Schema: public; Owner: dbuser
--

COPY public.record_k (recordid, userid, bookid, borrowdate, returndate, duedate) FROM stdin;
c3465a5a            	u001                	B001 	2025-04-15 00:00:00	2025-04-15 00:00:00	2025-06-14 00:00:00
3d5b847d            	u001                	B001 	2025-04-15 00:00:00	2025-04-15 00:00:00	2025-06-14 00:00:00
ebb8d3dc            	u001                	B001 	2025-04-15 00:00:00	2025-04-15 00:00:00	2025-06-14 00:00:00
fc939d10            	u001                	B114 	2025-04-15 00:00:00	2025-04-15 00:00:00	2025-06-14 00:00:00
5b29140f            	u001                	B114 	2025-04-15 00:00:00	2025-04-15 00:00:00	2025-06-14 00:00:00
ab0b3ea2            	u001                	B001 	2025-05-18 00:00:00	2025-05-18 00:00:00	2025-07-17 00:00:00
a28bd6c3            	u001                	B001 	2025-05-31 00:00:00	2025-05-31 00:00:00	2025-07-30 00:00:00
31e62cf3            	u001                	B001 	2025-06-19 00:00:00	2025-06-19 00:00:00	2025-08-18 00:00:00
3f7fb8f8            	u001                	B001 	2025-06-19 00:00:00	2025-09-19 00:00:00	2025-08-18 00:00:00
\.
;

--
-- Data for Name: user_k; Type: TABLE DATA; Schema: public; Owner: dbuser
--

COPY public.user_k (userid, username) FROM stdin;
u001                	张三              
u002                	李四              
u003                	王五              
u004                	赵六              
u005                	小红              
u006                	小明              
\.
;

--
-- Data for Name: user_login_k; Type: TABLE DATA; Schema: public; Owner: dbuser
--

COPY public.user_login_k (user_id, user_pass) FROM stdin;
u001                	123456              
u002                	123456              
u003                	123456              
u004                	123456              
u005                	123456              
u006                	123456              
\.
;

--
-- Name: admin_login_k_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE admin_login_k
    ADD CONSTRAINT admin_login_k_pkey PRIMARY KEY  (admin_id);


--
-- Name: book_k_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE book_k
    ADD CONSTRAINT book_k_pkey PRIMARY KEY  (bookid);


--
-- Name: record_k_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE record_k
    ADD CONSTRAINT record_k_pkey PRIMARY KEY  (recordid, userid, bookid, duedate);


--
-- Name: user_k_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE user_k
    ADD CONSTRAINT user_k_pkey PRIMARY KEY  (userid);


--
-- Name: user_login_k_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE user_login_k
    ADD CONSTRAINT user_login_k_pkey PRIMARY KEY  (user_id);


--
-- Name: record_k_bookid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE record_k
    ADD CONSTRAINT record_k_bookid_fkey FOREIGN KEY (bookid) REFERENCES book_k(bookid);


--
-- Name: record_k_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE record_k
    ADD CONSTRAINT record_k_userid_fkey FOREIGN KEY (userid) REFERENCES user_k(userid);


--
-- Name: public; Type: ACL; Schema: -; Owner: omm
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM omm;
GRANT CREATE,USAGE ON SCHEMA public TO omm;
GRANT USAGE ON SCHEMA public TO PUBLIC;


--
-- openGauss database dump complete
--

