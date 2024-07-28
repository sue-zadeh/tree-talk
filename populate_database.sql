
-- -----------------------------------------------------
-- Create Example Users
-- -----------------------------------------------------
-- User passwords are all just the username with "pass" appended:
--
-- User     Password
-- ------   --------
-- user1    user1pass
-- user2    user2pass
-- staff1   staff1pass
-- staff2   staff2pass
-- admin1   admin1pass
--
-- Hashes were generated using the included password_hash_generator.py script,
-- with the salt 'ExampleSaltValue'.
-- -----------------------------------------------------

USE TreeTalk;

-- Insert Example Users/Members
INSERT INTO users (username, first_name, last_name, email, password_hash, birth_date, location, role) VALUES
    ('user1', 'John', 'Smith', 'user1@example.com', '490cbfbe67bd8c617be3c6df6c829b6ac646ba3ae64f68f0a3cc284908855554', '01-01-1990', 'New Zealand', 'member'),
    ('user2', 'Helen', 'Green', 'user2@example.com', '2ffa2992addbd26a22490cc0a9b4bf7fa5ba2f218fccd3a57aaf299b7aa93dd9', '02-01-1989', 'New Zealand', 'member'),
    ('user3', 'Sue', 'Brown', 'user3@example.com', 'b69fda794abc570c3996aae5d8ac116db669cdf2dd55b205c6ae9c1a4bfb6d2a', '03-01-1988', 'New Zealand', 'member'),
    ('user4', 'Sarah', 'Jones', 'user4@example.com', '6ecfb27f2bb7236b72f6244eb15cc96fae1c5296a32e6f5867b705cf773c077b', '04-01-1987', 'New Zealand', 'member'),
    ('user5', 'Mary', 'Taylor', 'user5@example.com', '08650262ea4792f8607adf818216d72b42028456231efaa3c627607d0a68e0c5', '05-01-1986', 'New Zealand', 'member'),
    ('user6', 'Alice', 'Johnson', 'user6@example.com', 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6', '-02-01-1991', 'New Zealand', 'member'),
    ('user7', 'Bob', 'Williams', 'user7@example.com', 'b1c2d3e4f5g6h7i8j9k0l1m2n3o4p5q6', '-03-01-1992', 'New Zealand', 'member'),
    ('user8', 'Charlie', 'Brown', 'user8@example.com', 'c1d2e3f4g5h6i7j8k9l0m1n2o3p4q5r6', '-04-01-1993', 'New Zealand', 'member'),
    ('user9', 'Dave', 'Davis', 'user9@example.com', 'd1e2f3g4h5i6j7k8l9m0n1o2p3q4r5s6', '05-01-1994', 'New Zealand', 'member'),
    ('user10', 'Eve', 'White', 'user10@example.com', 'e1f2g3h4i5j6k7l8m9n0o1p2q3r4s5t6', '06-01-1995', 'New Zealand', 'member'),
    ('user11', 'Frank', 'Black', 'user11@example.com', 'f1g2h3i4j5k6l7m8n9o0p1q2r3s4t5u6', '07-01-1996', 'New Zealand', 'member'),
    ('user12', 'Grace', 'Green', 'user12@example.com', 'g1h2i3j4k5l6m7n8o9p0q1r2s3t4u5v6', '08-01-1997', 'New Zealand', 'member'),
    ('user13', 'Hank', 'Blue', 'user13@example.com', 'h1i2j3k4l5m6n7o8p9q0r1s2t3u4v5w6', '09-01-1985', 'New Zealand', 'member'),
    ('user14', 'Ivy', 'Red', 'user14@example.com', 'i1j2k3l4m5n6o7p8q9r0s1t2u3v4w5x6', '10-01-1978', 'New Zealand', 'member'),
    ('user15', 'Jack', 'Yellow', 'user15@example.com', 'j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6', '11-01-1978', 'New Zealand', 'member'),
    ('user16', 'Karen', 'Pink', 'user16@example.com', 'k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6', '12-01-1978', 'New Zealand', 'member'),
    ('user17', 'Leo', 'Gray', 'user17@example.com', 'l1m2n3o4p5q6r7s8t9u0v1w2x3y4z5a6', '01-01-1978', 'New Zealand', 'member'),
    ('user18', 'Mia', 'Purple', 'user18@example.com', 'm1n2o3p4q5r6s7t8u9v0w1x2y3z4a5b6', '02-01-1978', 'New Zealand', 'member'),
    ('user19', 'Nate', 'Orange', 'user19@example.com', 'n1o2p3q4r5s6t7u8v9w0x1y2z3a4b5c6', '03-01-1978', 'New Zealand', 'member'),
    ('user20', 'Olive', 'Silver', 'user20@example.com', 'o1p2q3r4s5t6u7v8w9x0y1z2a3b4c5d6', '04-01-1978', 'New Zealand', 'member'),
    ('user21', 'Paul', 'Gold', 'user21@example.com', 'p1q2r3s4t5u6v7w8x9y0z1a2b3c4d5e6', '05-01-1978', 'New Zealand', 'member'),
    ('user22', 'Quinn', 'Bronze', 'user22@example.com', 'q1r2s3t4u5v6w7x8y9z0a1b2c3d4e5f6', '06-01-1978', 'New Zealand', 'member');

-- Insert Example Moderators
INSERT INTO users (username, first_name, last_name, email, password_hash, birth_date, location, role) VALUES
    ('moderator1', 'Tony', 'Stark', 'moderator1@example.com', '6fcd6883408bf1760fd9f9953fe6b219d74488288de6b63a437bb2bdabb204f2', '06-01-1985', 'New Zealand', 'moderator'),
    ('moderator2', 'Mark', 'Ruffalo', 'moderator2@example.com', '37bb41f28154ad01ce2eac36cdd126385d173c9c7057587cee0fa78691f85aff', '07-01-1984', 'New Zealand', 'moderator'),
    ('moderator3', 'Bruce', 'Banner', 'moderator3@example.com', '48b349812f44490fa23629ebd7a474f63e994f839d4e3e01b4e6956839cfe2b8', '08-01-1986', 'New Zealand', 'moderator'),
    ('moderator4', 'Natasha', 'Romanoff', 'moderator4@example.com', '1b1a1bb8f30dba469db7fce99c92d5d9c65a4a9f1e780b9da93e2881a2899679', '09-01-1987', 'New Zealand', 'moderator'),
    ('moderator5', 'Clint', 'Barton', 'moderator5@example.com', 'a9b1bc8f07c7b8988f217bc7f5e1bce88e6f274c4da0a89aa9b73e5e7f573a81', '10-01-1988', 'New Zealand', 'moderator'),
    ('moderator6', 'Steve', 'Rogers', 'moderator6@example.com', '8c2b5d65e17fdd62e49f1c9c7e4b62d9d1a4e9c86e4a5c6d9dbe4e1c7a6d65e8', '11-01-1989', 'New Zealand', 'moderator'),
    ('moderator7', 'Thor', 'Odinson', 'moderator7@example.com', 'ebc8e8b1b0a8a9a9b8c8b7e8e9b9c9e7e6d9d8e9d8d7e9c8a8b8c7b6a9b8d7e6', '12-01-1990', 'New Zealand', 'moderator'),
    ('moderator8', 'Wanda', 'Maximoff', 'moderator8@example.com', 'f3e8b9c8a9a8b9c9e7e6e9c8a8a7e8c9e7d6e8b7a8c9a8e7e8c7e6a8b9a8c9d7', '01-01-1991', 'New Zealand', 'moderator'),
    ('moderator9', 'Vision', 'Vision', 'moderator9@example.com', 'a8a9b8c9d7e6c8e9a8b7a9e7e8c8d9e8c7d9e7e8c8a9a8b9e7c8a9b7c8a8b9e6', '02-01-1992', 'New Zealand', 'moderator'),
    ('moderator10', 'Sam', 'Wilson', 'moderator10@example.com', 'e7e8c9a8b8a9c8e7e8d9c8e8a7b9a8a9e8d7c8b9e8a9c8e8a7b8d7c8e8a9b9d7', '03-01-1993', 'New Zealand', 'moderator');

-- Insert Example Admins
INSERT INTO users (username, first_name, last_name, email, password_hash, birth_date, location, role) VALUES
    ('admin1', 'Jane', 'Doe', 'admin1@example.com', 'f96ccfe70a319f69019876d2be895235e7ee5d2b5f21dd51c6aa189b275acddf', '08-01-1983', 'New Zealand', 'admin'),
    ('admin2', 'John', 'Doe', 'admin2@example.com', 'c5f5d6b7e8a8e9d8e9c8e7d8b9c8a7e6d9e8d7e8a9b9c8e7d9e8b8a7e6a8b9e7', '09-01-1984', 'New Zealand', 'admin'),
    ('admin3', 'Alice', 'Wonder', 'admin3@example.com', 'd6e7c8a9b8c9e7e8d9c7e8a9b7c8e8d9e7a8b9e7e8c8a9b8e7d9c8a9b7e8d7e6', '10-01-1985', 'New Zealand', 'admin'),
    ('admin4', 'Bob', 'Builder', 'admin4@example.com', 'e8d7a9b8e9d7c8e7e8a9b8d9e7c8a8b9e7e8d9c8a9b7e8d9e7a8b8c9e7d9e8b8', '11-01-1986', 'New Zealand', 'admin');


-- Insert Messages
INSERT INTO messages (user_id, title, content) VALUES
(1, 'Welcome!', 'Welcome to our message board! Feel free to post any questions or messages.'),
(2, 'Moderation Guidelines', 'Please adhere to the community rules when posting.');

-- Insert Replies
INSERT INTO replies (message_id, user_id, content) VALUES
(1, 2, 'Thanks for the warm welcome!'),
(2, 1, 'Understood, thanks for the guidelines.');