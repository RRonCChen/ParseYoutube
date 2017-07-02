import requests
import pymysql


# VideoId ='5RhsO-tHjTg';
VideoId ='mayRuANk51w';
APIKey = '';

DataUrl = 'https://www.googleapis.com/youtube/v3/videos?id='+VideoId+'&key='+APIKey+'&part=statistics';
DataRes = requests.get(DataUrl);

conn = pymysql.connect(host='localhost', port=, user='', passwd='', db='',  charset="utf8mb4");
cur = conn.cursor();


def initUrl():

    #第一次初始化
    nextPageToken ='';
    CommentUrl = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet%2Creplies&maxResults=100&pageToken='+nextPageToken+'&videoId=' + VideoId + '&key=' + APIKey;

    CommentRes = requests.get(CommentUrl)
    nextPageToken = parseComment(CommentRes);

    #取的下一頁的Token
    while 1:
        if nextPageToken != '' :
            CommentUrl = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet%2Creplies&maxResults=100&pageToken=' + nextPageToken + '&videoId=' + VideoId + '&key=' + APIKey;
            CommentRes = requests.get(CommentUrl);
            nextPageToken = parseComment(CommentRes);
        else :
            break;

def parseComment(CommentRes):
     number_Comment =CommentRes.json()['pageInfo']['totalResults'];
     for i in range(0,number_Comment):
         Id =CommentRes.json()['items'][i]['id'];
         Author =CommentRes.json()['items'][i]['snippet']['topLevelComment']['snippet']['authorDisplayName'];
         Comment = CommentRes.json()['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'];
         LikeCount =CommentRes.json()['items'][i]['snippet']['topLevelComment']['snippet']['likeCount'];
         PublishAt = CommentRes.json()['items'][i]['snippet']['topLevelComment']['snippet']['updatedAt'];
         TotalReplyCount =(CommentRes.json()['items'][i]['snippet']['totalReplyCount']);

         # print('id : ' + CommentRes.json()['items'][i]['id']);
         # print('author : '+CommentRes.json()['items'][i]['snippet']['topLevelComment']['snippet']['authorDisplayName']);
         # print('comment : '+str(CommentRes.json()['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal']));
         # print('likeCount : '+str(CommentRes.json()['items'][i]['snippet']['topLevelComment']['snippet']['likeCount']));
         # print('publishAt : '+CommentRes.json()['items'][i]['snippet']['topLevelComment']['snippet']['updatedAt']);
         # print('totalReplyCount : ' + str(CommentRes.json()['items'][i]['snippet']['totalReplyCount']));
         # print('');

         cur.execute("INSERT INTO youtubedata (VideoId,Id,Author,Comment,LikeCount,PublishAt,TotalReplyCount) VALUES (%s,%s,%s,%s,%s,%s,%s)",[VideoId,Id,Author,Comment,LikeCount,PublishAt,TotalReplyCount])
         conn.commit();
     return CommentRes.json()['nextPageToken'];



initUrl();



