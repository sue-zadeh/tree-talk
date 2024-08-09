
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
INSERT INTO users (username, first_name, last_name, email, password, birth_date, location, role) VALUES
    ('user901', 'Bob', 'Builder', 'admin4@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '11-01-1986', 'New Zealand', 'admin');
    ('user900', 'Alice', 'Wonder', 'admin3@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '10-01-1985', 'New Zealand', 'admin'),
     ('user225', 'Elena', 'Leen', 'user225@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '01-01-1990', 'New Zealand', 'member'),
    ('user400', 'Sam', 'Wilson', 'moderator10@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '03-01-1993', 'New Zealand', 'moderator');
    ('user1', 'John', 'Smith', 'user1@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '01-01-1990', 'New Zealand', 'member'),
    ('user2', 'Helen', 'Green', 'user2@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '02-01-1989', 'New Zealand', 'member'),
    ('user3', 'Sue', 'Brown', 'user3@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '03-01-1988', 'New Zealand', 'member'),
    ('user4', 'Sarah', 'Jones', 'user4@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '04-01-1987', 'New Zealand', 'member'),
    ('user5', 'Mary', 'Taylor', 'user5@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '05-01-1986', 'New Zealand', 'member'),
    ('user6', 'Alice', 'Johnson', 'user6@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '-02-01-1991', 'New Zealand', 'member'),
    ('user7', 'Bob', 'Williams', 'user7@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '-03-01-1992', 'New Zealand', 'member'),
    ('user8', 'Charlie', 'Brown', 'user8@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '-04-01-1993', 'New Zealand', 'member'),
    ('user9', 'Dave', 'Davis', 'user9@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '05-01-1994', 'New Zealand', 'member'),
    ('user10', 'Eve', 'White', 'user10@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '06-01-1995', 'New Zealand', 'member'),
    ('user11', 'Frank', 'Black', 'user11@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '07-01-1996', 'New Zealand', 'member'),
    ('user12', 'Grace', 'Green', 'user12@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '08-01-1997', 'New Zealand', 'member'),
    ('user13', 'Hank', 'Blue', 'user13@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '09-01-1985', 'New Zealand', 'member'),
    ('user14', 'Ivy', 'Red', 'user14@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '10-01-1978', 'New Zealand', 'member'),
    ('user15', 'Jack', 'Yellow', 'user15@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '11-01-1978', 'New Zealand', 'member'),
    ('user16', 'Karen', 'Pink', 'user16@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '12-01-1978', 'New Zealand', 'member'),
    ('user17', 'Leo', 'Gray', 'user17@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '01-01-1978', 'New Zealand', 'member'),
    ('user18', 'Mia', 'Purple', 'user18@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '02-01-1978', 'New Zealand', 'member'),
    ('user119', 'Nate', 'Orange', 'user19@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '03-01-1978', 'New Zealand', 'member'),
    ('user210', 'Olive', 'Silver', 'user20@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '04-01-1978', 'New Zealand', 'member'),
    ('user211', 'Paul', 'Gold', 'user21@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '05-01-1978', 'New Zealand', 'member'),
    ('user222', 'Quinn', 'Bronze', 'user22@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '06-01-1978', 'New Zealand', 'member');
-- Moderators
    ('moderator1', 'Tony', 'Stark', 'moderator1@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '06-01-1985', 'New Zealand', 'moderator'),
    ('moderator2', 'Mark', 'Ruffalo', 'moderator2@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '07-01-1984', 'New Zealand', 'moderator'),
    ('moderator3', 'Bruce', 'Banner', 'moderator3@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '08-01-1986', 'New Zealand', 'moderator'),
    ('moderator4', 'Natasha', 'Romanoff', 'moderator4@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '09-01-1987', 'New Zealand', 'moderator'),
    ('moderator5', 'Clint', 'Barton', 'moderator5@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '10-01-1988', 'New Zealand', 'moderator'),
    ('user320', 'Steve', 'Rogers', 'moderator6@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '11-01-1989', 'New Zealand', 'moderator'),
    ('user300', 'Thor', 'Odinson', 'moderator7@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '12-01-1990', 'New Zealand', 'moderator'),
    ('user402', 'Wanda', 'Maximoff', 'moderator8@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '01-01-1991', 'New Zealand', 'moderator'),
    ('user401', 'Vision', 'Vision', 'moderator9@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '02-01-1992', 'New Zealand', 'moderator'),

-- Admins
    ('admin903', 'Jane', 'Doe', 'admin1@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '08-01-1983', 'New Zealand', 'admin'),
    ('user902 ', 'John', 'Doe', 'admin2@example.com', 'd16a34aaa4c4569dd7744189dc5c3e933a93aaaf01a9c098049b3dcc0468997f', '09-01-1984', 'New Zealand', 'admin'),


-- Insert Messages
INSERT INTO messages (user_id, title, content) VALUES
(1, 'Welcome!', 'Welcome to our message board! Feel free to post any questions or messages.'),
(2, 'Moderation Guidelines', 'Please adhere to the community rules when posting.'),
(3, 'Tree Care Tips', 'Here are some great tips for taking care of your trees.'),
(4, 'Landscaping Ideas', 'Discuss and share your landscaping ideas here.'),
(5, 'Pest Control', 'Effective ways to manage pests in your garden.'),
(6, 'Organic Gardening', 'Share your experiences with organic gardening.'),
(7, 'Seasonal Planting Guide', 'What to plant this season? Let\'s discuss.'),
(8, 'Watering Schedules', 'Best practices for watering your plants.'),
(9, 'Soil Management', 'How to maintain fertile soil.'),
(10, 'Pruning Techniques', 'Best techniques for pruning.'),
(11, 'Fruit Tree Care', 'Care tips for your fruit trees.'),
(12, 'Vegetable Gardening', 'Growing vegetables in your backyard.'),
(13, 'Herbal Gardens', 'Creating and managing an herbal garden.'),
(14, 'Composting Basics', 'How to start composting.'),
(15, 'Lawn Maintenance', 'Keeping your lawn green and healthy.'),
(16, 'Sustainable Practices', 'Discuss sustainable gardening practices.'),
(17, 'Indoor Plants', 'Care tips for indoor plants.'),
(18, 'Garden Tools Review', 'Review of the latest gardening tools.'),
(19, 'Community Events', 'Upcoming gardening and landscaping events.'),
(20, 'Wildlife in Gardens', 'How to attract and manage wildlife in your gardens.');



--Replies
INSERT INTO replies (message_id, user_id, content, parent_id) VALUES
(1, 2, 'Thanks for the warm welcome!', 1),
(2, 1, 'Understood, thanks for the guidelines.', 2),
(3, 3, 'Great tips, thanks!', 3),
(4, 4, 'Really helpful, thank you!', 4),
(5, 2, ''ve been looking for this info.', 5),
(6, 3, 'Absolutely agree with this point.', 6),
(7, 1, 'Interesting approach, thanks for sharing.', 7),
(8, 2, 'Helpful, was just planning my garden.', 8),
(9, 3, 'That's a useful tip!', 9),
(10, 1, 'Thanks, this was very needed.', 10);

-- Insert likes 
INSERT INTO likes (user_id, message_id, count type) VALUES
(1, 1, 3, 'like'),
(2, 2, 4, 'like'),
(3, 3, 1, 'like'),
(4, 4, 2, 'like');

-- Insert data into the media table
INSERT INTO media (message_id, filename) VALUES
(1, 'image1.png'),
(2, 'image2.jpg'),
(3, 'image3.gif'),
(1, 'image4.png'),
(2, 'image5.jpg');
