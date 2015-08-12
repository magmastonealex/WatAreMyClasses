//
//  TokenStorage.h
//  WatAreMyClasses
//
//  Created by Alex Roth on 2015-08-12.
//  Copyright © 2015 Alex Roth. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface TokenStorage : NSObject
@property (nonatomic) NSString *userID;
@property (nonatomic) NSString *token;
@property (nonatomic) NSUserDefaults * defaults;
+ (id)sharedStorage;
-(void)setUserID:(NSString*)uid withToken:(NSString*)ptoken;
@end
