CREATE TABLE "dim_project" (
  "project_id" int PRIMARY KEY,
  "project_name" varchar,
  "project_type" varchar,
  "client" varchar,
  "budget_million_usd" float,
  "complexity" varchar,
  "start_date" date,
  "end_date" date,
  "status" varchar
);

CREATE TABLE "dim_sequence" (
  "sequence_id" int PRIMARY KEY,
  "project_id" int,
  "sequence_name" varchar,
  "complexity" varchar,
  "start_date" date,
  "end_date" date,
  "status" varchar
);

CREATE TABLE "dim_shot" (
  "shot_id" int PRIMARY KEY,
  "project_id" int,
  "sequence_id" int,
  "shot_name" varchar,
  "complexity" varchar,
  "frame_count" int,
  "start_date" date,
  "end_date" date,
  "status" varchar
);

CREATE TABLE "dim_task" (
  "task_id" int PRIMARY KEY,
  "project_id" int,
  "sequence_id" int,
  "shot_id" int,
  "department" varchar,
  "estimated_hours" float,
  "priority" varchar,
  "start_date" date,
  "end_date" date,
  "status" varchar
);

CREATE TABLE "dim_artist" (
  "artist_id" int PRIMARY KEY,
  "artist_name" varchar,
  "department" varchar,
  "experience_years" float
);

CREATE TABLE "fact_task_assignment" (
  "assignment_id" int PRIMARY KEY,
  "task_id" int,
  "artist_id" int,
  "assigned_hours" float,
  "assignment_date" date
);

CREATE TABLE "fact_timesheet" (
  "timesheet_id" int PRIMARY KEY,
  "assignment_id" int,
  "artist_id" int,
  "work_date" date,
  "hours_logged" float
);

CREATE TABLE "fact_render_job" (
  "render_id" int PRIMARY KEY,
  "project_id" int,
  "sequence_id" int,
  "shot_id" int,
  "frame_count" int,
  "render_engine" varchar,
  "render_status" varchar,
  "render_hours" float,
  "submission_date" date,
  "completion_date" date
);

CREATE TABLE "fact_delivery" (
  "delivery_id" int PRIMARY KEY,
  "project_id" int,
  "sequence_id" int,
  "shot_id" int,
  "version" int,
  "delivery_date" date,
  "client_status" varchar,
  "review_days" float,
  "final_delivery" boolean
);

ALTER TABLE "dim_sequence" ADD FOREIGN KEY ("project_id") REFERENCES "dim_project" ("project_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "dim_shot" ADD FOREIGN KEY ("project_id") REFERENCES "dim_project" ("project_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "dim_shot" ADD FOREIGN KEY ("sequence_id") REFERENCES "dim_sequence" ("sequence_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "dim_task" ADD FOREIGN KEY ("project_id") REFERENCES "dim_project" ("project_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "dim_task" ADD FOREIGN KEY ("sequence_id") REFERENCES "dim_sequence" ("sequence_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "dim_task" ADD FOREIGN KEY ("shot_id") REFERENCES "dim_shot" ("shot_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "fact_task_assignment" ADD FOREIGN KEY ("task_id") REFERENCES "dim_task" ("task_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "fact_task_assignment" ADD FOREIGN KEY ("artist_id") REFERENCES "dim_artist" ("artist_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "fact_timesheet" ADD FOREIGN KEY ("assignment_id") REFERENCES "fact_task_assignment" ("assignment_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "fact_timesheet" ADD FOREIGN KEY ("artist_id") REFERENCES "dim_artist" ("artist_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "fact_render_job" ADD FOREIGN KEY ("project_id") REFERENCES "dim_project" ("project_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "fact_render_job" ADD FOREIGN KEY ("sequence_id") REFERENCES "dim_sequence" ("sequence_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "fact_render_job" ADD FOREIGN KEY ("shot_id") REFERENCES "dim_shot" ("shot_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "fact_delivery" ADD FOREIGN KEY ("project_id") REFERENCES "dim_project" ("project_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "fact_delivery" ADD FOREIGN KEY ("sequence_id") REFERENCES "dim_sequence" ("sequence_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "fact_delivery" ADD FOREIGN KEY ("shot_id") REFERENCES "dim_shot" ("shot_id") DEFERRABLE INITIALLY IMMEDIATE;
