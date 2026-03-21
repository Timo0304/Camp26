"""
Bible Quiz Game for Sunday School Camp '26
Fun, colorful Bible trivia for children and teens.
"""

QUESTIONS = {
    "Kids (Easy)": [
        {
            "question": "Who built the ark?",
            "options": ["Moses", "Noah", "David", "Abraham"],
            "answer": "Noah",
            "emoji": "🚢",
            "fun_fact": "Noah brought 2 of every animal onto the ark!"
        },
        {
            "question": "What did God create on the first day?",
            "options": ["Animals", "Light", "The Sea", "Trees"],
            "answer": "Light",
            "emoji": "💡",
            "fun_fact": "God said 'Let there be light' and there was light! (Genesis 1:3)"
        },
        {
            "question": "How many disciples did Jesus have?",
            "options": ["10", "7", "12", "15"],
            "answer": "12",
            "emoji": "👥",
            "fun_fact": "The 12 disciples followed Jesus everywhere and spread the Gospel!"
        },
        {
            "question": "What was the name of the garden where Adam and Eve lived?",
            "options": ["Garden of Gethsemane", "Garden of Eden", "Garden of Roses", "Garden of Life"],
            "answer": "Garden of Eden",
            "emoji": "🌿",
            "fun_fact": "The Garden of Eden was a perfect paradise created by God!"
        },
        {
            "question": "What food did God send from heaven to feed the Israelites?",
            "options": ["Bread", "Manna", "Fish", "Fruit"],
            "answer": "Manna",
            "emoji": "🍞",
            "fun_fact": "Manna appeared every morning like dew on the ground. God fed millions of people!"
        },
        {
            "question": "Who swallowed Jonah?",
            "options": ["A shark", "A whale", "A big fish", "A dolphin"],
            "answer": "A big fish",
            "emoji": "🐟",
            "fun_fact": "Jonah stayed inside the fish for 3 days and nights before it spat him out!"
        },
        {
            "question": "What did David use to defeat Goliath?",
            "options": ["A sword", "A spear", "A sling and stone", "His hands"],
            "answer": "A sling and stone",
            "emoji": "🪨",
            "fun_fact": "David was just a young shepherd boy when he defeated the giant Goliath!"
        },
        {
            "question": "What is the shortest verse in the Bible?",
            "options": ["God is love", "Jesus wept", "Pray always", "Fear not"],
            "answer": "Jesus wept",
            "emoji": "📖",
            "fun_fact": "'Jesus wept' is found in John 11:35 — only two words!"
        },
        {
            "question": "Who was thrown into the lions' den?",
            "options": ["Paul", "Daniel", "Elijah", "Joseph"],
            "answer": "Daniel",
            "emoji": "🦁",
            "fun_fact": "God sent an angel to shut the lions' mouths and Daniel was not harmed!"
        },
        {
            "question": "What did Jesus turn water into?",
            "options": ["Juice", "Milk", "Wine", "Oil"],
            "answer": "Wine",
            "emoji": "🍷",
            "fun_fact": "This was Jesus' very first miracle, at a wedding in Cana! (John 2:1-11)"
        },
    ],
    "Teens (Medium)": [
        {
            "question": "How many books are in the Bible?",
            "options": ["60", "66", "72", "64"],
            "answer": "66",
            "emoji": "📚",
            "fun_fact": "66 books — 39 in the Old Testament and 27 in the New Testament!"
        },
        {
            "question": "Who wrote most of the Psalms?",
            "options": ["Solomon", "Moses", "David", "Asaph"],
            "answer": "David",
            "emoji": "🎵",
            "fun_fact": "David wrote 73 of the 150 Psalms. He was also a talented musician!"
        },
        {
            "question": "In which city was Jesus born?",
            "options": ["Jerusalem", "Nazareth", "Bethlehem", "Jericho"],
            "answer": "Bethlehem",
            "emoji": "⭐",
            "fun_fact": "Bethlehem means 'House of Bread' in Hebrew. It fulfilled Micah 5:2!"
        },
        {
            "question": "Who betrayed Jesus for 30 pieces of silver?",
            "options": ["Peter", "Thomas", "Judas Iscariot", "Bartholomew"],
            "answer": "Judas Iscariot",
            "emoji": "😔",
            "fun_fact": "30 pieces of silver was the price of a slave in ancient times. (Zechariah 11:12)"
        },
        {
            "question": "What is the fruit of the Spirit listed FIRST in Galatians 5?",
            "options": ["Joy", "Peace", "Love", "Patience"],
            "answer": "Love",
            "emoji": "❤️",
            "fun_fact": "Love, Joy, Peace, Patience, Kindness, Goodness, Faithfulness, Gentleness, Self-control!"
        },
        {
            "question": "Which apostle walked on water with Jesus?",
            "options": ["John", "Peter", "James", "Andrew"],
            "answer": "Peter",
            "emoji": "🌊",
            "fun_fact": "Peter stepped out of the boat in faith, but sank when he took his eyes off Jesus!"
        },
        {
            "question": "What is the first book of the New Testament?",
            "options": ["Mark", "Luke", "John", "Matthew"],
            "answer": "Matthew",
            "emoji": "📖",
            "fun_fact": "Matthew was a tax collector before Jesus called him to be a disciple!"
        },
        {
            "question": "How many days did creation take according to Genesis?",
            "options": ["5", "6", "7", "10"],
            "answer": "6",
            "emoji": "🌍",
            "fun_fact": "God created everything in 6 days and rested on the 7th — which became the Sabbath!"
        },
        {
            "question": "Who was the first king of Israel?",
            "options": ["David", "Solomon", "Saul", "Samuel"],
            "answer": "Saul",
            "emoji": "👑",
            "fun_fact": "Saul was tall and handsome, but God said He looks at the heart, not outward appearance!"
        },
        {
            "question": "What does 'Immanuel' mean?",
            "options": ["King of kings", "God with us", "Prince of Peace", "Son of God"],
            "answer": "God with us",
            "emoji": "🙏",
            "fun_fact": "Isaiah 7:14 prophesied that the Messiah would be called Immanuel — God with us!"
        },
    ],
    "Champions (Hard)": [
        {
            "question": "How many years did the Israelites wander in the wilderness?",
            "options": ["20", "30", "40", "50"],
            "answer": "40",
            "emoji": "🏜️",
            "fun_fact": "40 years because of their unbelief at Kadesh Barnea. Only Joshua and Caleb entered Canaan!"
        },
        {
            "question": "Which prophet was taken to heaven in a chariot of fire?",
            "options": ["Elisha", "Isaiah", "Enoch", "Elijah"],
            "answer": "Elijah",
            "emoji": "🔥",
            "fun_fact": "Elijah never died! He was taken directly to heaven in a whirlwind with a chariot of fire!"
        },
        {
            "question": "What were Paul and Silas doing when the prison doors opened?",
            "options": ["Sleeping", "Praying and singing", "Fasting", "Preaching"],
            "answer": "Praying and singing",
            "emoji": "🎶",
            "fun_fact": "At midnight, while they praised God, an earthquake shook the prison and all doors opened! (Acts 16)"
        },
        {
            "question": "How many lepers did Jesus heal, but only one returned to say thank you?",
            "options": ["5", "7", "10", "12"],
            "answer": "10",
            "emoji": "🙌",
            "fun_fact": "Jesus asked 'Were not ten cleansed? Where are the nine?' Only a Samaritan returned to give thanks!"
        },
        {
            "question": "What is the longest chapter in the Bible?",
            "options": ["Psalm 118", "Psalm 119", "Isaiah 40", "Numbers 7"],
            "answer": "Psalm 119",
            "emoji": "📜",
            "fun_fact": "Psalm 119 has 176 verses and is an acrostic poem — each section starts with a Hebrew letter!"
        },
        {
            "question": "Who was the mother of John the Baptist?",
            "options": ["Mary", "Anna", "Elizabeth", "Miriam"],
            "answer": "Elizabeth",
            "emoji": "👶",
            "fun_fact": "Elizabeth was Mary's cousin! When Mary visited, baby John leaped in Elizabeth's womb for joy!"
        },
        {
            "question": "In Revelation, how many elders surround God's throne?",
            "options": ["12", "24", "144", "7"],
            "answer": "24",
            "emoji": "👑",
            "fun_fact": "24 elders wearing white robes and golden crowns, worshipping God day and night! (Revelation 4:4)"
        },
        {
            "question": "What was the name of Abraham's first son?",
            "options": ["Isaac", "Jacob", "Ishmael", "Esau"],
            "answer": "Ishmael",
            "emoji": "👦",
            "fun_fact": "Ishmael was born to Hagar. Isaac, the son of promise, came 14 years later!"
        },
        {
            "question": "Which book of the Bible contains the armor of God?",
            "options": ["Colossians", "Romans", "Ephesians", "Philippians"],
            "answer": "Ephesians",
            "emoji": "⚔️",
            "fun_fact": "Ephesians 6:10-18 lists the full armor of God — belt, breastplate, shoes, shield, helmet, sword!"
        },
        {
            "question": "How many stones did Solomon use to begin building the temple? (What year of his reign?)",
            "options": ["1st year", "4th year", "7th year", "10th year"],
            "answer": "4th year",
            "emoji": "🏛️",
            "fun_fact": "Solomon began building the temple in the 4th year of his reign, 480 years after the Exodus! (1 Kings 6:1)"
        },
    ]
}

LEVEL_COLORS = {
    "Kids (Easy)":      {"border": "#06D6A0", "bg": "#f0fff8", "badge": "#06D6A0", "shadow": "#04a87d"},
    "Teens (Medium)":   {"border": "#4CC9F0", "bg": "#f0faff", "badge": "#1A73E8", "shadow": "#1558b0"},
    "Champions (Hard)": {"border": "#C77DFF", "bg": "#faf0ff", "badge": "#7B2FBE", "shadow": "#5a2090"},
}

SCORE_MESSAGES = [
    (10, "🏆 PERFECT SCORE! You're a Bible Champion!"),
    (8,  "🌟 Amazing! You really know your Bible!"),
    (6,  "👍 Great job! Keep reading your Bible!"),
    (4,  "📖 Good try! The more you read, the more you know!"),
    (0,  "💪 Keep going! Every Bible champion started somewhere!"),
]
