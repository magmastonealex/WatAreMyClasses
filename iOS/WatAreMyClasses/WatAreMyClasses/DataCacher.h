//
//  DataCacher.h
//  WatAreMyClasses
//
//  Created by Alex Roth on 2015-08-11.
//  Copyright © 2015 Alex Roth. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "WatService.h"
@interface DataCacher : NSObject
@property (nonatomic) NSArray * classes;
@property (nonatomic) NSArray * buildings;
@property (nonatomic) WatService *watService;
@property (nonatomic) NSString * userID;
@property (nonatomic) NSString * token;
+ (id)sharedCache;
- (void)doCache;
@end
