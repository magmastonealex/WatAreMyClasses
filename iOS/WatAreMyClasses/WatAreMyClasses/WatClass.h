//
//  WatClass.h
//  WatAreMyClasses
//
//  Created by Alex Roth on 2015-08-07.
//  Copyright © 2015 Alex Roth. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <Mantle/Mantle.h>

@interface WatClass : MTLModel<MTLJSONSerializing>

@property (nonatomic) NSNumber *  cid;
@property (nonatomic) NSString * class_name;
@property (nonatomic) NSString * section;
@property (nonatomic) NSString * timestamp;
@property (nonatomic) NSString * timeend;
@property (nonatomic) NSString * instructor;
@property (nonatomic) NSString * type;
@property (nonatomic) NSString * where;

@end
