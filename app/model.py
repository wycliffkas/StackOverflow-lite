from flask import session

class Users :
    buckets = []

    ##Add buckets.
    def add_bucket(self, name, time):
        ## Check if the name and time have been provided.
        if name and time:
            ## Create a dictionary to hold the new item.
            #id = 1
            #if len(self.buckets):
            id = len(self.buckets) + 1

            user_id = session['user_id']
            dict = {'id': id, 'name': name, 'time': time, 'user_id': user_id}
            self.buckets.append(dict)
            return {'success' : True}

        return {'success' : False}

    ## Edit bucket
    def edit_bucket(self, bucket_id, name, time):
        bucket_id = int(bucket_id)
        if name:
            for bucket in self.buckets:
                if bucket['id'] == bucket_id:
                    bucket['name'] = name
                    bucket['time'] = time

            return {'success' : True}

        return {'success' : False}

    ## Delete bucket
    def delete_bucket(self, bucket_id):
        bucket_id = int(bucket_id)
        if id:
            for bucket in self.buckets:
                if bucket['id'] == bucket_id:
                    self.buckets.remove(bucket)

            return {'success' : True}
        return {'success' : False}

    ## List buckets.
    def list_items(self):
        user_id = session['user_id']
        bucket_listings = []
        for bucket in self.buckets:
            if bucket['user_id'] == user_id:
                bucket_listings.append(bucket)
                
        return bucket_listings   


class Bucket:
    bucketlist_items = []

    ##Add buckets items.
    def add_item(self, name, description, time, bucket_id):
        ## Check if the name and time have been provided.
        if name:
            ## Create a dictionary to hold the new item.
            item_id = len(self.bucketlist_items) + 1
            bucket_id = int(bucket_id)

            item_dict = {'id': item_id, 'name': str(name), 'description': str(description), 'time': str(time), 'bucket_id': bucket_id}
            #item_di = {'id': item_id, 'name': str(name)}
            #return item_di

            self.bucketlist_items.append(item_dict)
            
            #return self.bucketlist_items
            return {'success' : True}

        return {'success' : False}

    ## Edit bucket item
    def edit_item(self, item_id, name, description, time, bucket_id):
        ## The id cannnot be empty
        item_id = int(item_id)
        if item_id and name:
            for item in self.bucketlist_items:
                if item['id'] == item_id:
                    item['name'] = name
                    item['description'] = description
                
                    #return True
                    
            return {'success' : True}

    ## Delete bucket item
    def delete_item(self, item_id):
        item_id = int(item_id)
        if id:
            for item in self.bucketlist_items:
                if item['id'] == item_id:
                    self.bucketlist_items.remove(item)

            return {'success' : True}

    ## List buckets items.
    def bucket_items(self, bucket_id):
        items = [] # A list to hold the bucket items
        bucket_id = int(bucket_id)
        for bucket_item in self.bucketlist_items:
            if bucket_item['bucket_id'] == bucket_id:
                items.append(bucket_item)

        return items
        #return self.bucketlist_items

class BucketItem:        
    bucketItems = []