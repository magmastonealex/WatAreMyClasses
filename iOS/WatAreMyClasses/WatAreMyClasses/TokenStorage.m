//
//  TokenStorage.m
//  WatAreMyClasses
//
//  Created by Alex Roth on 2015-08-12.
//  Copyright © 2015 Alex Roth. All rights reserved.
//

#import "TokenStorage.h"
// A singleton to manage storage of tokens.
// All properties will remain null until first set.
// This allows "skip" functionality to work properly.
@implementation TokenStorage
@synthesize userID,token,defaults;
+ (id)sharedStorage {
    static TokenStorage *sharedstorage = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        sharedstorage = [[self alloc] init];
    });
    return sharedstorage;
}
-(id) init{
    self=[super init];
    if(self){
        self.defaults=[NSUserDefaults standardUserDefaults];
        //Uncomment to test skip functionality. Clears all saved stuff.
        //NSString *appDomain = [[NSBundle mainBundle] bundleIdentifier];
        //[[NSUserDefaults standardUserDefaults] removePersistentDomainForName:appDomain];
        
        self.userID=[defaults objectForKey:@"userid"];
        self.token=[defaults objectForKey:@"token"];
    }
    return self;
}
-(void)setUserID:(NSString*)uid withToken:(NSString*)ptoken{
    self.userID=uid;
    self.token=ptoken;
    [defaults setObject:uid forKey:@"userid"];
    [defaults setObject:ptoken forKey:@"token"];
    [defaults synchronize];
}
@end
