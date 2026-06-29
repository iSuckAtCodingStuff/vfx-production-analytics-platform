CREATE TABLE "dim_project" (
  "project_id" varchar(15) PRIMARY KEY NOT NULL,
  "project_name" varchar(100) NOT NULL,
  "project_type" varchar(30) NOT NULL,
  "client" varchar(100) NOT NULL,
  "budget_million_usd" numeric(10,2) NOT NULL,
  "complexity" varchar(20) NOT NULL,
  "start_date" date NOT NULL,
  "end_date" date,
  "status" varchar(20) NOT NULL
);

CREATE TABLE "dim_sequence" (
  "sequence_id" varchar(20) PRIMARY KEY NOT NULL,
  "project_id" varchar(15) NOT NULL,
  "sequence_name" varchar(100) NOT NULL,
  "complexity" varchar(20) NOT NULL,
  "start_date" date NOT NULL,
  "end_date" date,
  "status" varchar(20) NOT NULL
);

CREATE TABLE "dim_shot" (
  "shot_id" varchar(20) PRIMARY KEY NOT NULL,
  "sequence_id" varchar(20) NOT NULL,
  "shot_name" varchar(100) NOT NULL,
  "complexity" varchar(20) NOT NULL,
  "frame_count" int NOT NULL,
  "start_date" date NOT NULL,
  "end_date" date,
  "status" varchar(20) NOT NULL
);

CREATE TABLE "dim_task" (
  "task_id" varchar(20) PRIMARY KEY NOT NULL,
  "shot_id" varchar(20) NOT NULL,
  "department" varchar(50) NOT NULL,
  "estimated_hours" numeric(10,2) NOT NULL,
  "priority" varchar(20) NOT NULL,
  "start_date" date NOT NULL,
  "end_date" date,
  "status" varchar(20) NOT NULL
);

CREATE TABLE "dim_artist" (
  "artist_id" varchar(15) PRIMARY KEY NOT NULL,
  "artist_name" varchar(100) NOT NULL,
  "department" varchar(50) NOT NULL,
  "experience_years" numeric(4,1) NOT NULL
);

CREATE TABLE "fact_task_assignment" (
  "assignment_id" varchar(20) PRIMARY KEY NOT NULL,
  "task_id" varchar(20) NOT NULL,
  "artist_id" varchar(15) NOT NULL,
  "assigned_hours" numeric(10,2) NOT NULL,
  "assignment_date" date NOT NULL
);

CREATE TABLE "fact_timesheet" (
  "timesheet_id" varchar(20) PRIMARY KEY NOT NULL,
  "assignment_id" varchar(20) NOT NULL,
  "work_date" date NOT NULL,
  "hours_logged" numeric(10,2) NOT NULL
);

CREATE TABLE "fact_render_job" (
  "render_id" varchar(20) PRIMARY KEY NOT NULL,
  "shot_id" varchar(20) NOT NULL,
  "frame_count" int NOT NULL,
  "render_engine" varchar(50) NOT NULL,
  "render_status" varchar(20) NOT NULL,
  "render_hours" numeric(10,2) NOT NULL,
  "submission_date" date NOT NULL,
  "completion_date" date
);

CREATE TABLE "fact_delivery" (
  "delivery_id" varchar(20) PRIMARY KEY NOT NULL,
  "shot_id" varchar(20) NOT NULL,
  "version" int NOT NULL,
  "delivery_date" date NOT NULL,
  "client_status" varchar(30) NOT NULL,
  "review_days" numeric(10,2),
  "final_delivery" boolean NOT NULL
);

ALTER TABLE "dim_sequence" ADD FOREIGN KEY ("project_id") REFERENCES "dim_project" ("project_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "dim_shot" ADD FOREIGN KEY ("sequence_id") REFERENCES "dim_sequence" ("sequence_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "dim_task" ADD FOREIGN KEY ("shot_id") REFERENCES "dim_shot" ("shot_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "fact_task_assignment" ADD FOREIGN KEY ("task_id") REFERENCES "dim_task" ("task_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "fact_task_assignment" ADD FOREIGN KEY ("artist_id") REFERENCES "dim_artist" ("artist_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "fact_timesheet" ADD FOREIGN KEY ("assignment_id") REFERENCES "fact_task_assignment" ("assignment_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "fact_render_job" ADD FOREIGN KEY ("shot_id") REFERENCES "dim_shot" ("shot_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "fact_delivery" ADD FOREIGN KEY ("shot_id") REFERENCES "dim_shot" ("shot_id") DEFERRABLE INITIALLY IMMEDIATE;
