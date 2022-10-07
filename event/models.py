# Sport Class
class Sport:
    def __init__(self, name, image, date, time, status, price, location, rating, description):
        self.name = name
        self.image = image
        self.date = date
        self.time = time
        self.status= status
        self.price = price
        self.location = location
        self.rating = rating
        self.description = description
        self.comments = list()

    def add_comment(self, comment):
        self.comments.append(comment)

# Comment Class
class Comment:
    def __init__(self, user, text, created_at):
        self.user = user
        self.text = text
        self.created_at = created_at

    def __repr__(self):
        str = 'User {0}, \n Text {1}'
        str.format(self.user, self.text)
        return str